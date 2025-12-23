
export const PROJECT = {
  NAME: 'Password Authentication Research',
  COURSE_CODE: '20940',
  COURSE_NAME: 'Introduction to Cybersecurity',
  GROUP_SEED: '211245440',
};

export const STUDENTS = [
  {
    name: 'Stav Kdoshim',
    id: '322356551',
  },
  {
    name: 'Ofir Sasson',
    id: '203650296',
  },
];

export const API_BASE_URL = 'http://localhost:8000/api';

export const ROUTES = {
  HOME: 'home',
  LOGIN: 'login',
  DASHBOARD: 'dashboard',
};

export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  USER: 'auth_user',
};

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
  
  // Login Page
  LOGIN_TITLE: 'Login',
  LOGIN_USERNAME: 'Username',
  LOGIN_PASSWORD: 'Password',
  LOGIN_LOADING: 'Logging in...',
  
  // Dashboard
  DASHBOARD_LOGGED_IN: 'Logged in as',
  DASHBOARD_PASSWORD_STRENGTH: 'Password Strength',
  
  // Stats
  STAT_TOTAL: 'Total Attempts',
  STAT_SUCCESS: 'Successful',
  STAT_FAILED: 'Failed',
  STAT_RATE: 'Success Rate',
};