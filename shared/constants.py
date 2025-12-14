"""
Shared constants for Python (backend & attack scripts)
"""

# ============================================
# PROJECT CONFIGURATION
# ============================================

GROUP_SEED = 322356551 ^ 111111111  # XOR of team member IDs
PROJECT_NAME = "Password Authentication Research"
COURSE_CODE = "20940"

# ============================================
# PASSWORD CATEGORIES
# ============================================

class PasswordStrength:
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    ALL = [WEAK, MEDIUM, STRONG]

# ============================================
# HASH MODES
# ============================================

class HashMode:
    SHA256 = "sha256"
    BCRYPT = "bcrypt"
    ARGON2 = "argon2"
    ALL = [SHA256, BCRYPT, ARGON2]

# ============================================
# PROTECTION MODES
# ============================================

class ProtectionMode:
    NONE = "none"
    RATE_LIMIT = "rate_limit"
    LOCKOUT = "lockout"
    CAPTCHA = "captcha"
    TOTP = "totp"
    ALL = [NONE, RATE_LIMIT, LOCKOUT, CAPTCHA, TOTP]

# ============================================
# ATTACK CONFIGURATION
# ============================================

WEAK_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "password1", "123123", "1234567890", "000000",
    "abc123", "qwerty", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "sunshine", "princess",
    str(GROUP_SEED)
]

MEDIUM_PASSWORDS = [
    "Pass123!", "Welcome2024", "Hello@World", "Test1234!",
    "Admin@123", "User@2024", "Medium!Pass", "Spring#2024",
    "Winter@123", "Summer!456"
]

STRONG_PASSWORDS = [
    "Tr0ub4dor&3", "correcthorsebatterystaple",
    "P@ssw0rd!2024#Secure", "MyS3cur3P@ssw0rd!",
    "C0mpl3x!ty#2024", "Str0ng&S3cur3!",
    "Un6r34k@bl3#Pwd", "S3cur1ty!F1rst#",
    "P@$$w0rd!Str0ng", "Ultra!S3cur3#2024"
]

# ============================================
# USER GENERATION
# ============================================

USERS_PER_CATEGORY = 10
TOTAL_USERS = USERS_PER_CATEGORY * len(PasswordStrength.ALL)

# ============================================
# ATTACK LIMITS
# ============================================

class AttackLimits:
    MAX_ATTEMPTS_PER_TEST = 50000
    MAX_TIME_PER_TEST_SECONDS = 7200
    DEFAULT_DELAY_BETWEEN_ATTEMPTS = 0.1

# ============================================
# API ENDPOINTS
# ============================================

class Endpoints:
    LOGIN = "/api/auth/login"
    REGISTER = "/api/auth/register"
    USERS = "/api/auth/users"
    USER_BY_ID = "/api/auth/users/{id}"
    STATS = "/api/auth/stats"
    LOGS = "/api/logs"

# ============================================
# HTTP STATUS CODES
# ============================================

class StatusCodes:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    LOCKED = 423
    INTERNAL_SERVER_ERROR = 500