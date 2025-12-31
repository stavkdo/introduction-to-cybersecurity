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
    ProtectionMode,
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
    get_minutes_until_unlock,
    generate_captcha_code,
    get_captcha_code 
)


# JWT Token Creation
def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")


# Log attempt to file
def log_attempt_to_file(log_data: dict):
    try:
        with open(ATTEMPT_LOG_FILE, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        print(f"[ERROR] Log file write failed: {e}")


# Log attempt to database and file
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


# Find user by username
def find_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


# raise exception if user not found
def validate_user_exists(user: User, username: str):
    if not user:
        print(f"[FAILED] User not found: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


# check if account is locked
def check_account_lockout(user: User):
    if is_account_locked(user):
        minutes_left = get_minutes_until_unlock(user)
        print(f"[LOCKED] {user.username} ({minutes_left} min left)")
        
        raise HTTPException(
            status_code=423,
            detail=f"Account locked. Try again in {minutes_left} minutes."
        )

  
# check if captcha is required and validate
def check_captcha_requirement(user: User, captcha_code: str):
    from app.protection_service import generate_captcha_image   

    if requires_captcha(user):
        if not is_captcha_valid(user.username, captcha_code if captcha_code else ""):

            captcha_code_generated = generate_captcha_code(user.username)
            # Generate image
            captcha_image_base64 = generate_captcha_image(captcha_code_generated)
            
            print(f"[CAPTCHA] Required for {user.username}: {captcha_code_generated} (attempts: {user.failed_attempts})")
            
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "captcha_required",
                    "message": "CAPTCHA required",
                    "captcha_image": captcha_image_base64 
                }
            )
        
        print(f"[CAPTCHA] Validated for {user.username}")


# check if TOTP is required
def check_totp_requirement(user: User, db: Session) -> bool:
    from app.protection_service import generate_totp_code
    
    if not requires_totp(user):
        return False
    
    # If user doesn't have TOTP yet, generate it now
    if not user.totp_secret:
        user.totp_secret = generate_totp_code()
        db.commit() 
        print(f"[TOTP] Generated for {user.username}: {user.totp_secret}")
    else:
        print(f"[TOTP] Existing code for {user.username}: {user.totp_secret}")
    
    return True

# verify user password and handle failed attempts
def verify_user_password(user: User, password: str, db: Session):
    if not verify_password(password, user.password_hash, HashMode(user.hash_mode)):
        # Only track failed attempts for LOCKOUT and CAPTCHA modes
        if PROTECTION_MODE in [ProtectionMode.LOCKOUT, ProtectionMode.CAPTCHA]:
            user.failed_attempts += 1
            db.commit()
            apply_lockout(user, db)  # Only actually locks if LOCKOUT mode
            print(f"[FAILED] Wrong password: {user.username} (attempts: {user.failed_attempts}, mode: {PROTECTION_MODE.name})")
        else:
            # In NONE or TOTP mode, don't track attempts
            print(f"[FAILED] Wrong password: {user.username} (no tracking - mode: {PROTECTION_MODE.name})")
        
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        if user.failed_attempts > 0:
            print(f"[SUCCESS] Password correct. Resetting failed attempts for {user.username}")
            user.failed_attempts = 0
            db.commit()    


# verify user TOTP code and handle failed attempts
def verify_user_totp(user: User, totp_code: str, db: Session):
    print(f"[VERIFY_TOTP] Called with totp_code: '{totp_code}'")
    
    if not totp_code:
        print(f"[TOTP] Required for {user.username}")
        raise HTTPException(
            status_code=403,
            detail={"error": "totp_required", "message": "TOTP code required"}
        )
    
    print(f"[VERIFY_TOTP] Calling verify_totp_code...")
    if not verify_totp_code(user, totp_code):
        # In TOTP mode, we don't track failed attempts
        print(f"[TOTP] Invalid code for {user.username}")
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
    
    print(f"[TOTP] Validated for {user.username}")


# complete successful login
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