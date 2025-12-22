"""
Protection Service that handles lockout, CAPTCHA, and TOTP logic
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import pyotp

from app.config import (
    PROTECTION_MODE,
    ProtectionMode,
    MAX_FAILED_ATTEMPTS,
    LOCKOUT_DURATION_MINUTES,
    CAPTCHA_REQUIRED_AFTER,
)
from app.database import User

valid_captcha_tokens = set()



def is_account_locked(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.LOCKOUT:
        return False
    
    if not user.locked_until:
        return False
    
    if datetime.utcnow() < user.locked_until:
        return True
    
    user.locked_until = None
    return False


def requires_captcha(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.CAPTCHA:
        return False
    
    return user.failed_attempts >= CAPTCHA_REQUIRED_AFTER


def requires_totp(user: User) -> bool:
    if PROTECTION_MODE != ProtectionMode.TOTP:
        return False
    
    return user.totp_secret is not None


def is_captcha_valid(token: str) -> bool:
    if token and token in valid_captcha_tokens:
        valid_captcha_tokens.discard(token)
        return True
    return False


def verify_totp_code(user: User, code: str) -> bool:
    if not user.totp_secret:
        return False
    
    try:
        totp = pyotp.TOTP(user.totp_secret)
        return totp.verify(code, valid_window=1)
    
    except Exception as e:
        print(f"[ERROR] TOTP verification failed: {e}")
        return False


def apply_lockout(user: User, db: Session):
    if PROTECTION_MODE == ProtectionMode.LOCKOUT:
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            print(f"[LOCKOUT] {user.username} locked for {LOCKOUT_DURATION_MINUTES} min")


def reset_protection_state(user: User, db: Session):
    user.failed_attempts = 0
    user.locked_until = None
    db.commit()


def generate_captcha_token() -> str:
    import secrets
    token = secrets.token_hex(16)
    valid_captcha_tokens.add(token)
    return token


def get_minutes_until_unlock(user: User) -> int:
    if not user.locked_until:
        return 0
    delta = user.locked_until - datetime.utcnow()
    return max(0, int(delta.total_seconds() / 60) + 1)


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_totp_uri(user: User, issuer_name: str = "PasswordAuthResearch") -> str:
    if not user.totp_secret:
        return None
    
    totp = pyotp.TOTP(user.totp_secret)
    return totp.provisioning_uri(
        name=user.username,
        issuer_name=issuer_name
    )