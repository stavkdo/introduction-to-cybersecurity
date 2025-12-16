
# ============================================
# PROJECT INFORMATION
# ============================================

PROJECT_NAME = "Security Project"
COURSE_CODE = "20940"
COURSE_NAME = "Security in Computing Systems"
GROUP_SEED = 211245440  # Update with your actual XOR result

# ============================================
# PASSWORD CATEGORIES
# ============================================

class PasswordStrength:
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"

# ============================================
# API CONFIGURATION
# ============================================

API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

# ============================================
# TEXT CONTENT (for frontend via API or hardcoded)
# ============================================

TEXTS = {
    # Navbar
    "NAVBAR_TITLE": "Password Authentication Research",
    "NAVBAR_WELCOME": "Welcome",
    "NAVBAR_DASHBOARD": "Dashboard",
    "NAVBAR_LOGOUT": "Logout",
    "NAVBAR_LOGIN": "Login",
    
    # Home Page
    "HOME_TITLE": "Password Authentication Research",
    "HOME_SUBTITLE": f"Security Course {COURSE_CODE}",
    "HOME_DESCRIPTION": "This is a research project analyzing password authentication mechanisms and their resilience against common attack vectors.",
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

# ============================================
# STORAGE KEYS (for frontend localStorage)
# ============================================

STORAGE_KEYS = {
    "TOKEN": "token",
    "USER": "user",
}