// ============================================
// PROJECT INFO
// ============================================
export const PROJECT = {
  NAME: 'Password Authentication Research',
  COURSE_CODE: '20940',
  COURSE_NAME: 'Introduction to Cybersecurity',
  GROUP_SEED: 211245440,
};

// ============================================
// API & ROUTES
// ============================================
export const API_BASE_URL = 'http://localhost:8000/api';

export const ROUTES = {
  HOME: 'home',
  LOGIN: 'login',
  DASHBOARD: 'dashboard',
};

export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
};

// ============================================
// TEXT CONTENT
// ============================================
export const TEXT = {
  // Common
  WELCOME: 'Welcome',
  LOGIN: 'Login',
  LOGOUT: 'Logout',
  LOADING: 'Loading...',
  
  // Project
  PROJECT_TITLE: PROJECT.NAME,
  PROJECT_SUBTITLE: `Security Course ${PROJECT.COURSE_CODE}`,
  
  // Navigation
  NAV_DASHBOARD: 'Dashboard',
  
  // Home Page
  HOME_DESCRIPTION: 'This is a research project analyzing password authentication mechanisms and their resilience against common attack vectors.',
  HOME_GROUP_SEED_LABEL: 'Group Seed',
  HOME_CTA: 'Go to Login',
  
  // Login
  LOGIN_TITLE: 'Login',  
  LOGIN_USERNAME_PLACEHOLDER: 'Username',  
  LOGIN_PASSWORD_PLACEHOLDER: 'Password',  
  LOGIN_LOADING: 'Logging in...',  
  LOGIN_BUTTON: 'Login',  
  
  // Dashboard
  DASHBOARD_LOGGED_IN: 'Logged in as',
  DASHBOARD_PASSWORD_STRENGTH: 'Password Strength',
  
  // Stats
  STAT_TOTAL: 'Total Attempts',
  STAT_SUCCESS: 'Successful',
  STAT_FAILED: 'Failed',
  STAT_RATE: 'Success Rate',
};