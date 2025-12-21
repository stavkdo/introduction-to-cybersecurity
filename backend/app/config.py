import os
from dotenv import load_dotenv

load_dotenv()


PROJECT_NAME = "Password Authentication Research"
COURSE_CODE = "20940"
COURSE_NAME = "Introduction to Cybersecurity"
GROUP_SEED = os.getenv("GROUP_SEED", "1215067c7") 
DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
PEPPER = os.getenv("PEPPER", "default-pepper-change-in-production")

API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"


class PasswordStrength:
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


# Hash algorithm parameters
BCRYPT_COST = 12
ARGON2_TIME_COST = 1
ARGON2_MEMORY_COST = 64 * 1024  
ARGON2_PARALLELISM = 1

class HashMode:
    NONE = "none"
    SHA256 = "sha256"
    BCRYPT = "bcrypt"
    ARGON2ID = "argon2id"

class ProtectionFlag:
    NONE = 0
    RATE_LIMITING = 1 
    LOCKOUT = 2
    CAPTCHA = 3
    TOTP = 4
    PEPPER = 5

PROTECTION_FLAG = ProtectionFlag.NONE
HASH_MODE = HashMode.NONE

MAX_FAILED_ATTEMPTS = 5         # Lock account after 5 failed attempts
LOCKOUT_DURATION_MINUTES = 3    # Lock for 3 minutes
CAPTCHA_REQUIRED_AFTER = 3      # Show CAPTCHA after 3 failed attempts
MAX_ATTEMPTS_PER_FORM = 50000   # Default: up to 50,000 attempts per attack form
MAX_TOTAL_ATTEMPTS = 1000000    # Limit: up to 1,000,000 attempts total
MAX_RUNTIME_HOURS = 2           # Limit: up to 2 hours runtime (whichever comes first)

class AttackResult:
    SUCCESS = "success"
    FAILED = "failed"
    LOCKED = "locked"
    CAPTCHA_REQUIRED = "captcha_required"
    TOTP_REQUIRED = "totp_required"


ATTEMPT_LOG_FILE = "attempts.log"  # JSON lines format

STORAGE_KEYS = {
    "TOKEN": "auth_token",
    "USER": "auth_user",
}
