"""
FastAPI Application - Main API endpoints
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import time
import traceback

from app.database import get_db, User, AttemptLog
from app.config import (
    GROUP_SEED, PROTECTION_MODE, HASH_MODE, PROJECT_NAME, FRONTEND_URL,
    MAX_LOGIN_REQUESTS_PER_MINUTE, MAX_CAPTCHA_FAILED_ATTEMPTS,
    AttackResult, HashMode, PasswordStrength, ProtectionMode
)
from app.hash_utils import hash_password
from app.helpers import (
    find_user, validate_user_exists, validate_password,
    log_attempt, create_jwt_token
)
from app.protection_service import (
    cleanup_stale_protection_data, validate_account_not_locked,
    requires_captcha, validate_captcha, requires_totp, ensure_totp_exists,
    get_totp_code, validate_totp, check_rate_limit, apply_lockout,
    reset_protection_state, generate_captcha_code, generate_captcha_image,
    handle_invalid_captcha, handle_totp_required, handle_invalid_totp
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
    totp_code: str = None
    captcha_code: str = None


class LoginTOTPRequest(BaseModel):
    username: str
    password: str
    totp_code: str = None
    captcha_code: str = None




# Handle failed password attempt
def handle_failed_password(user: User, db: Session, start_time: float, ip: str):
    print(f"Password failed: {user.username}")
    
    # Increment attempts for LOCKOUT and CAPTCHA modes
    if PROTECTION_MODE in [ProtectionMode.LOCKOUT, ProtectionMode.CAPTCHA]:
        user.failed_attempts += 1
        db.commit()
        print(f"Failed attempts: {user.failed_attempts}")
        
        if PROTECTION_MODE == ProtectionMode.LOCKOUT:
            apply_lockout(user, db)
    
    # Show CAPTCHA if threshold reached
    if PROTECTION_MODE == ProtectionMode.CAPTCHA and user.failed_attempts >= MAX_CAPTCHA_FAILED_ATTEMPTS:
        code = generate_captcha_code(user.username, force_new=True)
        image = generate_captcha_image(code)
        
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.CAPTCHA_REQUIRED, user.username, HashMode(user.hash_mode), latency, ip)
        
        print(f"CAPTCHA required: {user.username} (attempts: {user.failed_attempts}/{MAX_CAPTCHA_FAILED_ATTEMPTS})")
        
        raise HTTPException(
            status_code=403,
            detail={
                "error": "captcha_required",
                "message": "CAPTCHA required after multiple failed attempts",
                "captcha_image": image
            }
        )
    
    # Regular failure
    latency = (time.time() - start_time) * 1000
    log_attempt(db, AttackResult.FAILED, user.username, HashMode(user.hash_mode), latency, ip)
    
    raise HTTPException(
        status_code=401,
        detail={"error": "invalid_credentials", "message": "Invalid username or password"}
    )



# Complete successful login
def handle_successful_login(user: User, db: Session, start_time: float, ip: str):
    reset_protection_state(user, db)
    
    latency = (time.time() - start_time) * 1000
    log_attempt(db, AttackResult.SUCCESS, user.username, HashMode(user.hash_mode), latency, ip)
    
    print(f"Login success: {user.username}")
    
    token = create_jwt_token(user.username)
    
    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {
            "username": user.username,
            "password_strength": user.password_strength
        }
    }


# Root endpoint - API info
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


# Register new user
@app.post("/api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid Username", "message": "Username already exists"}
        )
    
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
    
    print(f"User registered: {user.username} (hash={HASH_MODE.value})")
    
    return {
        "success": True,
        "message": "User registered",
        "user": {
            "username": user.username,
            "password_strength": user.password_strength
        }
    }


# Main login endpoint
@app.post("/api/login")
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"Login attempt: {request.username} from {ip} (mode={PROTECTION_MODE.name})")
    
    user = None
    
    if PROTECTION_MODE == ProtectionMode.RATE_LIMITING:
        check_rate_limit(ip, MAX_LOGIN_REQUESTS_PER_MINUTE, "login")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        print(f"User state: attempts={user.failed_attempts}, locked={bool(user.locked_until)}")
        
        cleanup_stale_protection_data(user, db)
        validate_account_not_locked(user)
        
        captcha_required = requires_captcha(user)
        captcha_valid = validate_captcha(user, request.captcha_code)
        
        password_correct = validate_password(user, request.password)
        
        if not password_correct:
            handle_failed_password(user, db, start_time, ip)
        
        if captcha_required and not captcha_valid:
            handle_invalid_captcha(user, db, start_time, ip)
        
        if requires_totp(user):
            ensure_totp_exists(user, db)
            handle_totp_required(user, db, start_time, ip)
        
        return handle_successful_login(user, db, start_time, ip)
    
    except HTTPException:
        raise
    
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "message": str(e)}
        )


# Login with TOTP verification
@app.post("/api/login_totp")
def login_totp(request: LoginTOTPRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"Login TOTP: {request.username} from {ip} (mode={PROTECTION_MODE.name})")
    
    user = None
    
    if PROTECTION_MODE == ProtectionMode.RATE_LIMITING:
        check_rate_limit(ip, MAX_LOGIN_REQUESTS_PER_MINUTE, "login")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        print(f"User state: attempts={user.failed_attempts}, locked={bool(user.locked_until)}")
        
        cleanup_stale_protection_data(user, db)
        validate_account_not_locked(user)
        
        # Check CAPTCHA if required
        captcha_required = requires_captcha(user)
        
        if captcha_required:
            captcha_valid = validate_captcha(user, request.captcha_code)
            if not captcha_valid:
                handle_invalid_captcha(user, db, start_time, ip)
        
        # Check password
        password_correct = validate_password(user, request.password)
        
        if not password_correct:
            ensure_totp_exists(user, db)
            handle_failed_password(user, db, start_time, ip)
        
        # Check TOTP mode enabled
        if not requires_totp(user):
            raise HTTPException(
                status_code=400,
                detail={"error": "totp_not_enabled", "message": "TOTP not enabled for this user"}
            )
        
        ensure_totp_exists(user, db)
        
        # Check if TOTP code provided
        if not request.totp_code:
            handle_totp_required(user, db, start_time, ip)
        
        # Validate TOTP code
        try:
            validate_totp(user, request.totp_code)
        except HTTPException:
            handle_invalid_totp(user, db, start_time, ip)
        
        return handle_successful_login(user, db, start_time, ip)
    
    except HTTPException:
        raise
    
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "message": str(e)}
        )


# Get TOTP code for user (for testing/attacks)
@app.get("/api/get_totp")
def get_totp(username: str, group_seed: str, db: Session = Depends(get_db)):
    if group_seed != GROUP_SEED:
        raise HTTPException(
            status_code=403,
            detail={"error": "Invalid group_seed", "message": "Invalid group_seed"}
        )
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": "Invalid user", "message": "User not found"}
        )
    
    code = get_totp_code(user)
    
    if not code:
        raise HTTPException(
            status_code=404,
            detail={"error": "Invalid user", "message": "User does not have TOTP enabled"}
        )
    
    print(f"TOTP requested: {username} = {code}")
    return {"totp_code": code}


# Get statistics (for frontend dashboard)
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
        "protection_mode": PROTECTION_MODE.name,
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