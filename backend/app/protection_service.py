"""
Protection Service - All protection-related logic
Lockout, CAPTCHA, TOTP, rate limiting, and protection validation
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
import string
import base64
from io import BytesIO

from app.config import (
    PROTECTION_MODE, ProtectionMode,
    MAX_FAILED_ATTEMPTS, LOCKOUT_DURATION_MINUTES,
    MAX_CAPTCHA_FAILED_ATTEMPTS
)
from app.database import User
from captcha.image import ImageCaptcha


# In-memory storage
active_captcha_codes = {}
rate_limit_requests = {}


# Check if account is currently locked
def is_account_locked(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.LOCKOUT:
        return False
    
    if not user.locked_until:
        return False
    
    if datetime.utcnow() < user.locked_until:
        return True
    
    user.locked_until = None
    user.failed_attempts = 0
    print(f"Lockout expired: {user.username}")
    return False


# Apply lockout if threshold reached
def apply_lockout(user: User, db: Session):
    if PROTECTION_MODE == ProtectionMode.LOCKOUT:
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            db.commit()
            print(f"Locked: {user.username} for {LOCKOUT_DURATION_MINUTES}min")


# Get remaining lockout time in minutes
def get_minutes_until_unlock(user: User) -> int:
    if not user.locked_until:
        return 0
    delta = user.locked_until - datetime.utcnow()
    return max(0, int(delta.total_seconds() / 60) + 1)


# Raise 423 if account is locked
def validate_account_not_locked(user: User):
    if is_account_locked(user):
        minutes_left = get_minutes_until_unlock(user)
        print(f"Account locked: {user.username} ({minutes_left}min left)")
        raise HTTPException(
            status_code=423,
            detail={"error": "Locked", "message": f"Account locked. Try again in {minutes_left} minutes."}
        )


# Check if CAPTCHA is required for this user
def requires_captcha(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.CAPTCHA:
        return False
    return user.failed_attempts >= MAX_CAPTCHA_FAILED_ATTEMPTS


# Validate CAPTCHA code
def is_captcha_valid(username: str, code: str) -> bool:
    print(f"Validating CAPTCHA for {username}: '{code}'")
    
    if not code or username not in active_captcha_codes:
        return False
    
    captcha_data = active_captcha_codes[username]
    
    if datetime.utcnow() > captcha_data["expires"]:
        del active_captcha_codes[username]
        return False
    
    if code.upper() == captcha_data["code"]:
        del active_captcha_codes[username]
        return True
    
    return False


# Generate random 5-character CAPTCHA code
def generate_captcha_code(username: str, force_new: bool = False) -> str:
    if force_new or username not in active_captcha_codes:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        active_captcha_codes[username] = {
            "code": code,
            "expires": datetime.utcnow() + timedelta(minutes=5)
        }
        print(f"CAPTCHA generated for {username}: {code}")
        return code
    
    return active_captcha_codes[username]["code"]


# Generate CAPTCHA image and return as base64
def generate_captcha_image(code: str) -> str:
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(code)
    buffered = BytesIO(data.read())
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_base64


# Get active CAPTCHA code for user (for testing/attacks)
def get_captcha_code(username: str) -> str:
    if username in active_captcha_codes:
        return active_captcha_codes[username]["code"]
    return None


# Check if CAPTCHA is valid - returns True/False
def validate_captcha(user: User, captcha_code: str) -> bool:
    if not requires_captcha(user):
        return True
    
    is_valid = is_captcha_valid(user.username, captcha_code if captcha_code else "")
    print(f"CAPTCHA {user.username}: {'Valid' if is_valid else 'Invalid'}")
    return is_valid


# Check if TOTP is required
def requires_totp(user: User) -> bool:
    return PROTECTION_MODE == ProtectionMode.TOTP


# Verify TOTP code
def verify_totp_code(user: User, code: str) -> bool:
    if not user.totp_secret:
        return False
    return str(user.totp_secret).strip() == str(code).strip()


# Generate simple 6-digit TOTP code
def generate_totp_code() -> str:
    return ''.join(random.choices(string.digits, k=6))


# Get user's TOTP code (for testing/attacks)
def get_totp_code(user: User) -> str:
    return user.totp_secret if user.totp_secret else None


# Generate TOTP if doesn't exist
def ensure_totp_exists(user: User, db: Session):
    if not user.totp_secret:
        user.totp_secret = generate_totp_code()
        db.commit()
        print(f"TOTP generated for {user.username}: {user.totp_secret}")
    else:
        print(f"TOTP exists for {user.username}: {user.totp_secret}")


# Raise 401 if TOTP code is invalid
def validate_totp(user: User, totp_code: str):
    if not totp_code:
        print(f"TOTP missing: {user.username}")
        raise HTTPException(
            status_code=403,
            detail={"error": "totp_required", "message": "TOTP code required"}
        )
    
    if not verify_totp_code(user, totp_code):
        print(f"TOTP invalid: {user.username}")
        raise HTTPException(
            status_code=401,
            detail={"error": "totp_required", "message": "Invalid TOTP code"}
        )
    
    print(f"TOTP valid: {user.username}")


# Check and enforce rate limit
def check_rate_limit(ip: str, max_per_minute: int, endpoint: str):
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=60)
    
    if ip not in rate_limit_requests:
        rate_limit_requests[ip] = []
    
    rate_limit_requests[ip] = [
        (ts, ep) for ts, ep in rate_limit_requests[ip] if ts > cutoff
    ]
    
    endpoint_requests = [
        ts for ts, ep in rate_limit_requests[ip] if ep == endpoint
    ]
    
    if len(endpoint_requests) >= max_per_minute:
        oldest = min(endpoint_requests)
        retry_after = int((oldest + timedelta(seconds=60) - now).total_seconds())
        print(f"Rate limit exceeded: {ip} on {endpoint} ({len(endpoint_requests)}/{max_per_minute})")
        raise HTTPException(
            status_code=429,
            detail={"error": "Rate limiting", "message": f"Too many requests. Try again in {retry_after} seconds."}
        )
    
    rate_limit_requests[ip].append((now, endpoint))
    print(f"Rate limit OK: {ip} {len(endpoint_requests) + 1}/{max_per_minute} on {endpoint}")


# Reset protection state on successful login
def reset_protection_state(user: User, db: Session):
    user.failed_attempts = 0
    user.locked_until = None
    
    if user.username in active_captcha_codes:
        del active_captcha_codes[user.username]
    
    db.commit()
    print(f"Protection reset: {user.username}")


# Clean up protection data that doesn't match current mode
def cleanup_stale_protection_data(user: User, db: Session):
    changed = False
    
    print(f"Cleanup {user.username}: mode={PROTECTION_MODE.name}, attempts={user.failed_attempts}, locked={bool(user.locked_until)}, totp={bool(user.totp_secret)}")
    
    match PROTECTION_MODE:
        case ProtectionMode.NONE | ProtectionMode.RATE_LIMITING:
            if user.failed_attempts > 0:
                user.failed_attempts = 0
                changed = True
            if user.locked_until:
                user.locked_until = None
                changed = True
            if user.totp_secret:
                user.totp_secret = None
                changed = True
            if user.username in active_captcha_codes:
                del active_captcha_codes[user.username]
        
        case ProtectionMode.LOCKOUT:
            if user.totp_secret:
                user.totp_secret = None
                changed = True
            if user.username in active_captcha_codes:
                del active_captcha_codes[user.username]
        
        case ProtectionMode.CAPTCHA:
            if user.locked_until:
                user.locked_until = None
                changed = True
            if user.totp_secret:
                user.totp_secret = None
                changed = True
        
        case ProtectionMode.TOTP:
            if user.failed_attempts > 0:
                user.failed_attempts = 0
                changed = True
            if user.locked_until:
                user.locked_until = None
                changed = True
            if user.username in active_captcha_codes:
                del active_captcha_codes[user.username]
    
    if changed:
        db.commit()
        print(f"Cleanup done: attempts={user.failed_attempts}, locked={bool(user.locked_until)}, totp={bool(user.totp_secret)}")