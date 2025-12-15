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
// TEXT CONTENT (Reusable)
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
  LOGIN_USERNAME: 'Username',
  LOGIN_PASSWORD: 'Password',
  LOGIN_SUBMITTING: 'Logging in...',
  
  // Dashboard
  DASHBOARD_LOGGED_IN: 'Logged in as',
  DASHBOARD_PASSWORD_STRENGTH: 'Password Strength',
  
  // Stats
  STAT_TOTAL: 'Total Attempts',
  STAT_SUCCESS: 'Successful',
  STAT_FAILED: 'Failed',
  STAT_RATE: 'Success Rate',
};

// ============================================
// COLORS (Single source of truth)
// ============================================
export const COLORS = {
  PRIMARY: '#3498db',
  PRIMARY_DARK: '#2980b9',
  SUCCESS: '#27ae60',
  ERROR: '#e74c3c',
  WARNING: '#f39c12',
  INFO: '#34495e',
  BACKGROUND: '#ecf0f1',
  TEXT_PRIMARY: '#2c3e50',
  TEXT_SECONDARY: '#7f8c8d',
  BORDER: '#ddd',
  WHITE: '#ffffff',
};