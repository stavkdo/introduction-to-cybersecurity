"""
Protection Service
Handles lockout, CAPTCHA, and TOTP logic
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import random
import string

from app.config import (
    PROTECTION_MODE,
    ProtectionMode,
    MAX_FAILED_ATTEMPTS,
    LOCKOUT_DURATION_MINUTES,
    MAX_CAPTCHA_FAILED_ATTEMPTS,
)
from app.database import User
from captcha.image import ImageCaptcha
import base64
from io import BytesIO


# Captcha Format: {username: {"code": "A3X7K", "expires": datetime}}
active_captcha_codes = {}


# Check if account is locked
def is_account_locked(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.LOCKOUT:
        return False
    
    if not user.locked_until:
        return False
    
    if datetime.utcnow() < user.locked_until:
        return True
    
    user.locked_until = None
    user.failed_attempts = 0
    print(f"[LOCKOUT_EXPIRED] {user.username} - failed_attempts reset to 0")
    return False


# Check if CAPTCHA is required
def requires_captcha(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.CAPTCHA:
        return False
    
    return user.failed_attempts >= MAX_CAPTCHA_FAILED_ATTEMPTS


# Check if TOTP is required
def requires_totp(user: User) -> bool:
    return PROTECTION_MODE == ProtectionMode.TOTP


# Validate CAPTCHA code
def is_captcha_valid(username: str, code: str) -> bool:
    print(f"[CAPTCHA_CHECK] Validating for {username}, received code: '{code}'")
    if not code:
        return False
    
    # Check if user has active CAPTCHA
    if username not in active_captcha_codes:
        return False
    
    captcha_data = active_captcha_codes[username]
    
    # Check expiration (5 minutes)
    if datetime.utcnow() > captcha_data["expires"]:
        del active_captcha_codes[username]
        return False
    
    # Check code (case-insensitive)
    if code.upper() == captcha_data["code"]:
        del active_captcha_codes[username]  # Single use
        return True
    
    return False


# Verify TOTP code (simple static code)
def verify_totp_code(user: User, code: str) -> bool:
    if not user.totp_secret:
        return False
    
    return str(user.totp_secret).strip() == str(code).strip()


# Apply lockout if threshold reached
def apply_lockout(user: User, db: Session):
    if PROTECTION_MODE == ProtectionMode.LOCKOUT:
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            print(f"[LOCKOUT] {user.username} locked for {LOCKOUT_DURATION_MINUTES} min")


# Reset on successful login
def reset_protection_state(user: User, db: Session):
    user.failed_attempts = 0
    user.locked_until = None
    
    # Clear CAPTCHA if exists
    if user.username in active_captcha_codes:
        del active_captcha_codes[user.username]
    
    db.commit()
    print(f"[RESET] {user.username} - failed_attempts reset to 0")

# Generate random 5-character CAPTCHA code
def generate_captcha_code(username: str, force_new: bool = False) -> str:
    # If forcing new or doesn't exist, generate fresh code
    if force_new or username not in active_captcha_codes:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        
        active_captcha_codes[username] = {
            "code": code,
            "expires": datetime.utcnow() + timedelta(minutes=5)
        }
        
        print(f"[CAPTCHA] Generated NEW code for {username}: {code}")
        return code
    
    # Return existing code
    return active_captcha_codes[username]["code"]


# Generate CAPTCHA image and return as base64
def generate_captcha_image(code: str) -> str:
    image = ImageCaptcha(width=280, height=90)
    
    # Generate image
    data = image.generate(code)
    
    # Convert to base64
    buffered = BytesIO(data.read())
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return img_base64


# Get active CAPTCHA code for user (for testing/attacks)
def get_captcha_code(username: str) -> str:
    if username in active_captcha_codes:
        return active_captcha_codes[username]["code"]
    return None


# Get minutes until unlock
def get_minutes_until_unlock(user: User) -> int:
    if not user.locked_until:
        return 0
    delta = user.locked_until - datetime.utcnow()
    return max(0, int(delta.total_seconds() / 60) + 1)


# Generate simple 6-digit TOTP code
def generate_totp_code() -> str:
    return ''.join(random.choices(string.digits, k=6))


# Get user's TOTP code (for testing/attacks)
def get_totp_code(user: User) -> str:
    if user.totp_secret is not None:
        return user.totp_secret
    return None

# Clean up protection data that's not needed for current mode
def cleanup_stale_protection_data(user: User, db: Session):
    changed = False
    
    if PROTECTION_MODE not in [ProtectionMode.LOCKOUT, ProtectionMode.CAPTCHA]:
        if user.failed_attempts > 0:
            user.failed_attempts = 0
            changed = True
        if user.locked_until is not None:
            user.locked_until = None
            changed = True
    
    if changed:
        db.commit()
        print(f"[CLEANUP] Cleared stale protection data for {user.username}")


# Rate Limiting
rate_limit_requests = {}
def check_rate_limit(ip: str, max_per_minute: int = 10, endpoint: str = "login"):
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=60)
    
    if ip not in rate_limit_requests:
        rate_limit_requests[ip] = []
    
    rate_limit_requests[ip] = [
        (ts, ep) for ts, ep in rate_limit_requests[ip]
        if ts > cutoff
    ]
    
    endpoint_requests = [
        ts for ts, ep in rate_limit_requests[ip]
        if ep == endpoint
    ]
    
    if len(endpoint_requests) >= max_per_minute:
        oldest = min(endpoint_requests)
        retry_after = int((oldest + timedelta(seconds=60) - now).total_seconds())
        
        print(f"[RATE_LIMIT] {ip} exceeded limit for {endpoint} ({len(endpoint_requests)}/{max_per_minute})")
        
        from fastapi import HTTPException
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {retry_after} seconds."
        )
    
    rate_limit_requests[ip].append((now, endpoint))
    print(f"[RATE_LIMIT] {ip} - {len(endpoint_requests) + 1}/{max_per_minute} requests for {endpoint}")