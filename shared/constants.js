/**
 * Shared constants for JavaScript (frontend)
 */

// ============================================
// PROJECT CONFIGURATION
// ============================================

export const GROUP_SEED = 211245440;
export const PROJECT_NAME = 'Password Authentication Research';
export const COURSE_CODE = '20940';

// ============================================
// API CONFIGURATION
// ============================================

export const API_BASE_URL = 'http://localhost:8000/api';

// ============================================
// ROUTES
// ============================================

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
};

// ============================================
// PASSWORD CATEGORIES
// ============================================

export const PasswordStrength = {
  WEAK: 'weak',
  MEDIUM: 'medium',
  STRONG: 'strong',
};

// ============================================
// HASH MODES
// ============================================

export const HashMode = {
  SHA256: 'sha256',
  BCRYPT: 'bcrypt',
  ARGON2: 'argon2',
};

// ============================================
// PROTECTION MODES
// ============================================

export const ProtectionMode = {
  NONE: 'none',
  RATE_LIMIT: 'rate_limit',
  LOCKOUT: 'lockout',
  CAPTCHA: 'captcha',
  TOTP: 'totp',
};

// ============================================
// API ENDPOINTS
// ============================================

export const Endpoints = {
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  USERS: '/auth/users',
  USER_BY_ID: (id) => `/auth/users/${id}`,
  STATS: '/auth/stats',
  LOGS: '/logs',
};

// ============================================
// MESSAGES
// ============================================

export const MESSAGES = {
  LOGIN_SUCCESS: 'Login successful!',
  LOGOUT_SUCCESS: 'Logged out successfully',
  LOGIN_FAILED: 'Invalid credentials',
  ACCOUNT_LOCKED: 'Account is locked. Try again later.',
  SERVER_ERROR: 'Server error. Please try again.',
  NETWORK_ERROR: 'Network error. Check your connection.',
  USERNAME_REQUIRED: 'Username is required',
  USERNAME_MIN_LENGTH: 'Username must be at least 3 characters',
  PASSWORD_REQUIRED: 'Password is required',
};

// ============================================
// VALIDATION RULES
// ============================================

export const ValidationRules = {
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 100,
  PASSWORD_MIN_LENGTH: 1,
  PASSWORD_MAX_LENGTH: 255,
};

// ============================================
// HTTP STATUS CODES
// ============================================

export const StatusCodes = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  LOCKED: 423,
  INTERNAL_SERVER_ERROR: 500,
};

// ============================================
// LOCAL STORAGE KEYS
// ============================================

export const StorageKeys = {
  TOKEN: 'token',
  USER: 'user',
};