import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# DATABASE
# ============================================
DATABASE_URL = os.getenv("DATABASE_URL")


# ============================================
# SECURITY
# ============================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
GROUP_SEED = os.getenv("GROUP_SEED", "1215067c7")


# ============================================
# ACCOUNT LOCKOUT
# ============================================
MAX_FAILED_ATTEMPTS = 5  # Lock after 5 failed attempts
LOCKOUT_DURATION_MINUTES = 5  # Lock for 5 minutes


# ============================================
# RATE LIMITING
# ============================================
MAX_ATTEMPTS_PER_FORM = 50000  # Max attempts per attack form
MAX_TOTAL_ATTEMPTS = 1000000   # Max total attempts
MAX_RUNTIME_HOURS = 2          # Max 2 hours runtime


# ============================================
# CAPTCHA
# ============================================
CAPTCHA_REQUIRED_AFTER = 3  # Show CAPTCHA after 3 failed attempts


# ============================================
# HASH PARAMETERS
# ============================================
# bcrypt
BCRYPT_COST = 12

# Argon2id
ARGON2_TIME_COST = 1
ARGON2_MEMORY_COST = 64 * 1024  
ARGON2_PARALLELISM = 1

# Pepper (loaded from environment, not stored in DB)
PEPPER = os.getenv("PEPPER", "default-pepper-change-in-production")


# ============================================
# PROTECTION FLAGS (bit flags)
# ============================================
PROTECTION_NONE = 0
PROTECTION_RATE_LIMITING = 1 << 0  # 1
PROTECTION_LOCKOUT = 1 << 1        # 2
PROTECTION_CAPTCHA = 1 << 2        # 4
PROTECTION_TOTP = 1 << 3           # 8
PROTECTION_PEPPER = 1 << 4         # 16


# ============================================
# HASH MODES
# ============================================
HASH_SHA256 = "sha256"
HASH_BCRYPT = "bcrypt"
HASH_ARGON2ID = "argon2id"