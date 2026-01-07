"""
Configuration Module
"""
import os
from enum import Enum, IntEnum
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "Introduction to Cybersecurity"
GROUP_SEED = os.getenv("GROUP_SEED", "1215067c7")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
PEPPER = os.getenv("PEPPER", "default-pepper")
FRONTEND_URL = "http://localhost:5173"


class PasswordStrength(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class HashMode(str, Enum):
    PLAIN = "plain"
    SHA256 = "sha256"
    BCRYPT = "bcrypt"
    ARGON2ID = "argon2id"


class ProtectionMode(IntEnum):
    NONE = 0
    LOCKOUT = 1
    CAPTCHA = 2
    TOTP = 3
    RATE_LIMITING = 4


class AttackResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    LOCKED = "locked"
    CAPTCHA_REQUIRED = "captcha_required"
    TOTP_REQUIRED = "totp_required"


# ACTIVE CONFIGURATION - CHANGE TO TEST
PROTECTION_MODE = ProtectionMode.TOTP
HASH_MODE = HashMode.PLAIN

# PROTECTION SETTINGS
MAX_FAILED_ATTEMPTS = 5
MAX_CAPTCHA_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION_MINUTES = 3
MAX_LOGIN_REQUESTS_PER_MINUTE = 10

# Hash parameters
BCRYPT_COST = 12
ARGON2_TIME_COST = 1
ARGON2_MEMORY_COST = 64 * 1024
ARGON2_PARALLELISM = 1

ATTEMPT_LOG_FILE = "attempts.log"