"""
Password Hashing Utilities
"""
import hashlib
import secrets
import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.config import (
    BCRYPT_COST,
    ARGON2_TIME_COST,
    ARGON2_MEMORY_COST,
    ARGON2_PARALLELISM,
    PEPPER,
    HashMode
)

argon2_hasher = PasswordHasher(
    time_cost=ARGON2_TIME_COST,
    memory_cost=ARGON2_MEMORY_COST,
    parallelism=ARGON2_PARALLELISM
)



def hash_password(password: str, hash_mode: HashMode) -> str:
    match hash_mode:
        case HashMode.PLAIN:
            return password
        
        case HashMode.SHA256:
            salt = secrets.token_hex(16)
            combined = f"{password}{salt}{PEPPER}"
            hashed = hashlib.sha256(combined.encode()).hexdigest()
            return f"{hashed}:{salt}"
        
        case HashMode.BCRYPT:
            password_with_pepper = f"{password}{PEPPER}"
            hashed = bcrypt.hashpw(
                password_with_pepper.encode(),
                bcrypt.gensalt(rounds=BCRYPT_COST)
            )
            return hashed.decode()
        
        case HashMode.ARGON2ID:
            password_with_pepper = f"{password}{PEPPER}"
            return argon2_hasher.hash(password_with_pepper)
        
        case _:
            raise ValueError(f"Unknown hash mode: {hash_mode}")


def verify_password(password: str, stored_hash: str, hash_mode: HashMode) -> bool:
    try:
        match hash_mode:
            case HashMode.PLAIN:
                return password == stored_hash
            
            case HashMode.SHA256:
                if ":" not in stored_hash:
                    return False
                hashed, salt = stored_hash.split(":", 1)
                combined = f"{password}{salt}{PEPPER}"
                computed_hash = hashlib.sha256(combined.encode()).hexdigest()
                return computed_hash == hashed
            
            case HashMode.BCRYPT:
                password_with_pepper = f"{password}{PEPPER}"
                return bcrypt.checkpw(
                    password_with_pepper.encode(),
                    stored_hash.encode()
                )
            
            case HashMode.ARGON2ID:
                password_with_pepper = f"{password}{PEPPER}"
                argon2_hasher.verify(stored_hash, password_with_pepper)
                return True
            
            case _:
                return False
    
    except (VerifyMismatchError, ValueError, Exception) as e:
        print(f"[ERROR] Password verification failed: {e}")
        return False