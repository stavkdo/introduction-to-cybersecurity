"""
Helper Functions - General utilities
JWT, logging, user queries, and basic validation
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
import json

from app.database import User, AttemptLog
from app.config import (
    HashMode, AttackResult, SECRET_KEY, GROUP_SEED, 
    PROTECTION_MODE, ATTEMPT_LOG_FILE
)
from app.hash_utils import verify_password



# Create JWT token for authenticated user
def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")


# Write attempt to log file
def log_attempt_to_file(log_data: dict):
    try:
        with open(ATTEMPT_LOG_FILE, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        print(f"ERROR: Log write failed: {e}")


# Log attempt to both database and file
def log_attempt(db: Session, result: AttackResult, username: str, 
                hash_mode: HashMode, latency_ms: float, ip: str):
    attempt = AttemptLog(
        timestamp=datetime.utcnow(),
        group_seed=GROUP_SEED,
        username=username,
        hash_mode=hash_mode.value,
        protection_flags=PROTECTION_MODE.name,
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
        "protection_flags": PROTECTION_MODE.name,
        "result": result.value,
        "latency_ms": latency_ms
    })


# Find user by username
def find_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


# Raise 401 if user doesn't exist
def validate_user_exists(user: User, username: str):
    if not user:
        print(f"User not found: {username}")
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid credentials", "message": "Invalid username or password"}
        )


# Check if password is correct - returns True/False
def validate_password(user: User, password: str) -> bool:
    is_valid = verify_password(password, user.password_hash, HashMode(user.hash_mode))
    print(f"Password {user.username}: {'Correct' if is_valid else 'Wrong'}")
    return is_valid