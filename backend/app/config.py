"""
Configuration for Password Authentication Research
All constants, settings, and configuration in one place
"""
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

class HashMode:
    SHA256 = "sha256"
    BCRYPT = "bcrypt"
    ARGON2ID = "argon2id"

# Hash algorithm parameters
BCRYPT_COST = 12
ARGON2_TIME_COST = 1
ARGON2_MEMORY_COST = 64 * 1024  
ARGON2_PARALLELISM = 1

class ProtectionFlag:
    NONE = 0
    RATE_LIMITING = 1 << 0  # 1
    LOCKOUT = 1 << 1        # 2
    CAPTCHA = 1 << 2        # 4
    TOTP = 1 << 3           # 8
    PEPPER = 1 << 4         # 16


MAX_FAILED_ATTEMPTS = 5  # Lock account after X failed attempts
LOCKOUT_DURATION_MINUTES = 15  # Lock for X minutes
CAPTCHA_REQUIRED_AFTER = 3  # Show CAPTCHA after X failed attempts
MAX_ATTEMPTS_PER_FORM = 50000  # Default: up to 50,000 attempts per attack form
MAX_TOTAL_ATTEMPTS = 1000000   # Limit: up to 1,000,000 attempts total
MAX_RUNTIME_HOURS = 2          # Limit: up to 2 hours runtime (whichever comes first)

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


TEXTS = {
    # Project
    "PROJECT_NAME": PROJECT_NAME,
    "COURSE_CODE": COURSE_CODE,
    
    # Navbar
    "NAVBAR_TITLE": "Password Authentication Research",
    "NAVBAR_WELCOME": "Welcome",
    "NAVBAR_DASHBOARD": "Dashboard",
    "NAVBAR_LOGOUT": "Logout",
    "NAVBAR_LOGIN": "Login",
    
    # Home Page
    "HOME_TITLE": "Password Authentication Research",
    "HOME_SUBTITLE": f"Security Course {COURSE_CODE}",
    "HOME_DESCRIPTION": "Research project analyzing password authentication mechanisms and their resilience against common attack vectors.",
    "HOME_GROUP_SEED": "Group Seed",
    "HOME_LOGIN_BUTTON": "Go to Login",
    
    # Login Page
    "LOGIN_TITLE": "Login",
    "LOGIN_USERNAME_PLACEHOLDER": "Username",
    "LOGIN_PASSWORD_PLACEHOLDER": "Password",
    "LOGIN_BUTTON": "Login",
    "LOGIN_LOADING": "Logging in...",
    
    # Dashboard
    "DASHBOARD_TITLE": "Dashboard",
    "DASHBOARD_LOGGED_IN": "Logged in as",
    "DASHBOARD_PASSWORD_STRENGTH": "Password Strength",
    "DASHBOARD_LOADING": "Loading...",
    "DASHBOARD_TOTAL_ATTEMPTS": "Total Attempts",
    "DASHBOARD_SUCCESSFUL": "Successful",
    "DASHBOARD_FAILED": "Failed",
    "DASHBOARD_SUCCESS_RATE": "Success Rate",
}