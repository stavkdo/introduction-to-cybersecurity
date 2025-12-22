"""
Main Application
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import time

from app.database import get_db, User, AttemptLog
from app.config import (
    GROUP_SEED, PROTECTION_MODE, HASH_MODE, PROJECT_NAME, FRONTEND_URL,
    AttackResult, HashMode, PasswordStrength
)
from app.hash_utils import hash_password
from app.protection_service import generate_captcha_token, is_account_locked
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
    captcha_token: str = None


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


@app.post("/api/login")
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"[LOGIN] {request.username} from {ip}")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        check_account_lockout(user)
        check_captcha_requirement(user, request.captcha_token)
        
        verify_user_password(user, request.password, db)
        
        if check_totp_requirement(user):
            latency = (time.time() - start_time) * 1000
            log_attempt(db, AttackResult.TOTP_REQUIRED, user.username, HashMode(user.hash_mode), latency, ip)
            
            print(f"[TOTP] Required for {user.username}")
            
            raise HTTPException(
                status_code=403,
                detail={"error": "totp_required", "message": "Use /api/login_totp endpoint"}
            )
        
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.SUCCESS, user.username, HashMode(user.hash_mode), latency, ip)
        
        return complete_successful_login(user, db)
    
    except HTTPException:
        raise
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/login_totp")
def login_totp(request: LoginTOTPRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"[LOGIN_TOTP] {request.username} from {ip}")
    
    try:
        user = find_user(db, request.username)
        validate_user_exists(user, request.username)
        
        check_account_lockout(user)
        check_captcha_requirement(user, request.captcha_token)
        
        verify_user_password(user, request.password, db)
        verify_user_totp(user, request.totp_code, db)
        
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.SUCCESS, user.username, HashMode(user.hash_mode), latency, ip)
        
        return complete_successful_login(user, db)
    
    except HTTPException:
        raise
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_attempt(db, AttackResult.FAILED, request.username, HASH_MODE, latency, ip)
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/admin/get_captcha_token")
def get_captcha_token(group_seed: int):
    if group_seed != GROUP_SEED:
        raise HTTPException(status_code=403, detail="Invalid group_seed")
    
    token = generate_captcha_token()
    print(f"[ADMIN] CAPTCHA token: {token[:8]}...")
    
    return {"captcha_token": token}


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


@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    return {
        "total": len(users),
        "users": [
            {
                "username": user.username,
                "password_strength": user.password_strength,
                "hash_mode": user.hash_mode,
                "has_totp": user.totp_secret is not None if hasattr(user, 'totp_secret') else False,
                "failed_attempts": user.failed_attempts,
                "is_locked": is_account_locked(user)
            }
            for user in users
        ]
    }


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
