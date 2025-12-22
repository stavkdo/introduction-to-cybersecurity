"""
Helper Functions
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
import json

from app.database import User, AttemptLog
from app.config import (
    HashMode,
    AttackResult,
    SECRET_KEY,
    GROUP_SEED,
    PROTECTION_MODE,
    ATTEMPT_LOG_FILE
)
from app.hash_utils import verify_password
from app.protection_service import (
    is_account_locked,
    requires_captcha,
    requires_totp,
    is_captcha_valid,
    verify_totp_code,
    apply_lockout,
    reset_protection_state,
    get_minutes_until_unlock
)



def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")



def log_attempt_to_file(log_data: dict):
    try:
        with open(ATTEMPT_LOG_FILE, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        print(f"[ERROR] Log file write failed: {e}")



def log_attempt(db: Session, result: AttackResult, username: str, hash_mode: HashMode, latency_ms: float, ip: str):
    attempt = AttemptLog(
        timestamp=datetime.utcnow(),
        group_seed=GROUP_SEED,
        username=username,
        hash_mode=hash_mode.value,
        protection_flags=PROTECTION_MODE.value,
        result=result.value,
        latency_ms=latency_ms,
        ip_address=ip
    )
    db.add(attempt)
    db.commit()
    
    log_attempt_to_file({
        "timestamp": datetime.utcnow().isoformat(),
        "group_seed": GROUP_SEED,
        "username": username,
        "hash_mode": hash_mode.value,
        "protection_flags": PROTECTION_MODE.value,
        "result": result.value,
        "latency_ms": latency_ms
    })



def find_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()



def validate_user_exists(user: User, username: str):
    if not user:
        print(f"[FAILED] User not found: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")



def check_account_lockout(user: User):
    if is_account_locked(user):
        minutes_left = get_minutes_until_unlock(user)
        print(f"[LOCKED] {user.username} ({minutes_left} min left)")
        
        raise HTTPException(
            status_code=423,
            detail=f"Account locked. Try again in {minutes_left} minutes."
        )



def check_captcha_requirement(user: User, captcha_token: str):
    if requires_captcha(user):
        if not is_captcha_valid(captcha_token):
            print(f"[CAPTCHA] Required for {user.username}")
            
            raise HTTPException(
                status_code=403,
                detail={"error": "captcha_required", "message": "CAPTCHA required"}
            )
        
        print(f"[CAPTCHA] Validated for {user.username}")



def check_totp_requirement(user: User) -> bool:
    return requires_totp(user)



def verify_user_password(user: User, password: str, db: Session):
    if not verify_password(password, user.password_hash, HashMode(user.hash_mode)):
        user.failed_attempts += 1
        apply_lockout(user, db)
        db.commit()
        
        print(f"[FAILED] Wrong password: {user.username} (attempts: {user.failed_attempts})")
        raise HTTPException(status_code=401, detail="Invalid credentials")



def verify_user_totp(user: User, totp_code: str, db: Session):
    if not totp_code:
        print(f"[TOTP] Required for {user.username}")
        
        raise HTTPException(
            status_code=403,
            detail={"error": "totp_required", "message": "TOTP code required"}
        )
    
    if not verify_totp_code(user, totp_code):
        user.failed_attempts += 1
        apply_lockout(user, db)
        db.commit()
        
        print(f"[TOTP] Invalid code for {user.username}")
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
    
    print(f"[TOTP] Validated for {user.username}")



def complete_successful_login(user: User, db: Session) -> dict:
    reset_protection_state(user, db)
    
    print(f"[SUCCESS] {user.username}")
    
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