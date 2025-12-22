export const PROJECT = {
  NAME: 'Password Authentication Research',
  COURSE_CODE: '20940',
  COURSE_NAME: 'Introduction to Cybersecurity',
  GROUP_SEED: '1215067c7',
};


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
  WELCOME: 'Welcome',
  LOGIN: 'Login',
  LOGOUT: 'Logout',
  LOADING: 'Loading...',
  PROJECT_TITLE: PROJECT.NAME,
  PROJECT_SUBTITLE: `Security Course ${PROJECT.COURSE_CODE}`,
  NAV_DASHBOARD: 'Dashboard',
  HOME_DESCRIPTION: 'This is a research project analyzing password authentication mechanisms and their resilience against common attack vectors.',
  HOME_GROUP_SEED_LABEL: 'Group Seed',
  HOME_CTA: 'Go to Login',
  LOGIN_TITLE: 'Login',
  LOGIN_USERNAME: 'Username',
  LOGIN_PASSWORD: 'Password',
  LOGIN_LOADING: 'Logging in...',
  DASHBOARD_LOGGED_IN: 'Logged in as',
  DASHBOARD_PASSWORD_STRENGTH: 'Password Strength',
  STAT_TOTAL: 'Total Attempts',
  STAT_SUCCESS: 'Successful',
  STAT_FAILED: 'Failed',
  STAT_RATE: 'Success Rate',
};