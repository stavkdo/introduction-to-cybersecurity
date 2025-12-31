"""
FastAPI Application
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import time

from app.database import get_db, User, AttemptLog
from app.config import (
    GROUP_SEED, PROTECTION_MODE, HASH_MODE, PROJECT_NAME, FRONTEND_URL, MAX_LOGIN_REQUESTS_PER_MINUTE,
    AttackResult, HashMode, PasswordStrength, ProtectionMode
)
from app.hash_utils import hash_password
from app.protection_service import check_rate_limit, requires_captcha
from app.helpers import (
    find_user, validate_user_exists, check_account_lockout,
    check_captcha_requirement, check_totp_requirement,
    verify_user_password, verify_user_totp, complete_successful_login,
    log_attempt
)

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterRequest(BaseModel):
    username: str
    password: str
    password_strength: PasswordStrength = PasswordStrength.MEDIUM


class LoginRequest(BaseModel):
    username: str
    password: str
    captcha_code: str = None


class LoginTOTPRequest(BaseModel):
    username: str
    password: str
    totp_code: str
    captcha_token: str = None



@app.get("/")
def root():
    return {
        "message": "Password Auth Research API",
        "group_seed": GROUP_SEED,
        "current_config": {
            "hash_mode": HASH_MODE.value,
            "protection_mode": PROTECTION_MODE.name,
        },
        "endpoints": {
            "register": "/api/register",
            "login": "/api/login",
            "login_totp": "/api/login_totp",
            "stats": "/api/stats"
        },
        "status": "running"
    }


@app.post("/api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    password_hash = hash_password(request.password, HASH_MODE)
    
    user = User(
        username=request.username,
        password_hash=password_hash,
        password_strength=request.password_strength.value,
        hash_mode=HASH_MODE.value,
        failed_attempts=0,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    print(f"[REGISTER] {user.username} (hash={HASH_MODE.value})")
    
    return {
        "success": True,
        "message": "User registered",
        "user": {
            "username": user.username,
            "password_strength": user.password_strength
        }
    }


# Main login endpoint
# Parameters: username, password, captcha_code (optional)
# Returns: token on success, or error with protection requirements (CAPTCHA/TOTP)
@app.post("/api/login")
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"[LOGIN] {request.username} from {ip}")
    
    user = None
    result = AttackResult.FAILED
    
    if PROTECTION_MODE == ProtectionMode.RATE_LIMITING:
        check_rate_limit(ip, MAX_LOGIN_REQUESTS_PER_MINUTE, "login")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        from app.protection_service import cleanup_stale_protection_data
        cleanup_stale_protection_data(user, db)
        
        check_account_lockout(user)
        check_captcha_requirement(user, request.captcha_code)
        
        verify_user_password(user, request.password, db)
        
        if check_totp_requirement(user, db):
            latency = (time.time() - start_time) * 1000
            log_attempt(db, AttackResult.TOTP_REQUIRED, user.username, HashMode(user.hash_mode), latency, ip)
            
            print(f"[TOTP] Required for {user.username}: {user.totp_secret}")
            
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "totp_required", 
                    "message": "Two-Factor Authentication required",
                    "totp_code": user.totp_secret
                }
            )
        
        result = AttackResult.SUCCESS
        latency = (time.time() - start_time) * 1000
        log_attempt(db, result, user.username, HashMode(user.hash_mode), latency, ip)
        return complete_successful_login(user, db)
    
    except HTTPException as http_exc:
        latency = (time.time() - start_time) * 1000
        
        if http_exc.status_code == 423:
            result = AttackResult.LOCKED
        elif http_exc.status_code == 403:
            if user and isinstance(http_exc.detail, dict):
                if http_exc.detail.get("error") == "captcha_required":
                    result = AttackResult.CAPTCHA_REQUIRED
                elif http_exc.detail.get("error") == "totp_required":
                    result = AttackResult.TOTP_REQUIRED
        else:
            result = AttackResult.FAILED
            
            if user and PROTECTION_MODE == ProtectionMode.CAPTCHA and requires_captcha(user):
                from app.protection_service import generate_captcha_code, generate_captcha_image
                
                new_captcha_code = generate_captcha_code(user.username, force_new=True)
                new_captcha_image = generate_captcha_image(new_captcha_code)
                
                print(f"[CAPTCHA] Regenerated after wrong password: {new_captcha_code}")
                
                http_exc.detail = {
                    "error": "captcha_required",
                    "message": "Invalid credentials. New CAPTCHA generated.",
                    "captcha_image": new_captcha_image
                }
                http_exc.status_code = 403
                result = AttackResult.CAPTCHA_REQUIRED
        
        username = user.username if user else request.username
        hash_mode = HashMode(user.hash_mode) if user else HASH_MODE
        log_attempt(db, result, username, hash_mode, latency, ip)       
        raise
    
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Login endpoint with TOTP verification
# Parameters: username, password, totp_code, captcha_code (optional)
# Returns: token on success after validating TOTP code
@app.post("/api/login_totp")
def login_totp(request: LoginTOTPRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"[LOGIN_TOTP] {request.username} from {ip}")
    
    user = None
    result = AttackResult.FAILED

    if PROTECTION_MODE == ProtectionMode.RATE_LIMITING:
        check_rate_limit(ip, MAX_LOGIN_REQUESTS_PER_MINUTE, "login")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        from app.protection_service import cleanup_stale_protection_data
        cleanup_stale_protection_data(user, db)

        check_account_lockout(user)
        check_captcha_requirement(user, request.captcha_code)
        
        verify_user_password(user, request.password, db)
        check_totp_requirement(user, db)
        verify_user_totp(user, request.totp_code, db)
        
        result = AttackResult.SUCCESS
        latency = (time.time() - start_time) * 1000
        log_attempt(db, result, user.username, HashMode(user.hash_mode), latency, ip)
        
        return complete_successful_login(user, db)
    
    except HTTPException as http_exc:
        latency = (time.time() - start_time) * 1000
        
        if http_exc.status_code == 423:
            result = AttackResult.LOCKED
        elif http_exc.status_code == 403:
            if user and isinstance(http_exc.detail, dict):
                if http_exc.detail.get("error") == "captcha_required":
                    result = AttackResult.CAPTCHA_REQUIRED
                elif http_exc.detail.get("error") == "totp_required":
                    result = AttackResult.TOTP_REQUIRED
        else:
            result = AttackResult.FAILED
            
            if user and PROTECTION_MODE == ProtectionMode.CAPTCHA and requires_captcha(user):
                from app.protection_service import generate_captcha_code, generate_captcha_image
                
                new_captcha_code = generate_captcha_code(user.username, force_new=True)
                new_captcha_image = generate_captcha_image(new_captcha_code)
                
                print(f"[CAPTCHA] Regenerated after wrong password/TOTP: {new_captcha_code}")
                
                http_exc.detail = {
                    "error": "captcha_required",
                    "message": "Invalid credentials. New CAPTCHA generated.",
                    "captcha_image": new_captcha_image
                }
                http_exc.status_code = 403
                result = AttackResult.CAPTCHA_REQUIRED
        
        username = user.username if user else request.username
        hash_mode = HashMode(user.hash_mode) if user else HASH_MODE
        log_attempt(db, result, username, hash_mode, latency, ip)
        
        raise
    
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Get TOTP code for user (for testing/attacks)
# Parameters: username, group_seed
# Returns: totp_code for this user
@app.get("/api/get_totp")
def get_totp(username: str, group_seed: str, db: Session = Depends(get_db)):
    from app.protection_service import get_totp_code
    
    if group_seed != GROUP_SEED:
        raise HTTPException(status_code=403, detail="Invalid group_seed")
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    code = get_totp_code(user)
    
    if not code:
        raise HTTPException(status_code=404, detail="User does not have TOTP enabled")
    
    print(f"[ADMIN] TOTP code requested for {username}: {code}")    
    return {"totp_code": code}


# for frontend usage in dashboard
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(AttemptLog).count()
    successful = db.query(AttemptLog).filter(AttemptLog.result == AttackResult.SUCCESS.value).count()
    failed = db.query(AttemptLog).filter(AttemptLog.result == AttackResult.FAILED.value).count()
    locked = db.query(AttemptLog).filter(AttemptLog.result == AttackResult.LOCKED.value).count()
    captcha_required = db.query(AttemptLog).filter(AttemptLog.result == AttackResult.CAPTCHA_REQUIRED.value).count()
    totp_required = db.query(AttemptLog).filter(AttemptLog.result == AttackResult.TOTP_REQUIRED.value).count()
    
    return {
        "total_attempts": total,
        "successful": successful,
        "failed": failed,
        "locked": locked,
        "captcha_required": captcha_required,
        "totp_required": totp_required,
        "success_rate": round((successful / total * 100), 2) if total > 0 else 0
    }


# Get current system configuration (for frontend)
@app.get("/api/config")
def get_config():
    return {
        "protection_mode": PROTECTION_MODE.name,  # "NONE", "LOCKOUT", "CAPTCHA", "TOTP"
        "hash_mode": HASH_MODE.value,
        "group_seed": GROUP_SEED
    }


# Health check endpoint
@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        user_count = db.query(User).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "users": user_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }