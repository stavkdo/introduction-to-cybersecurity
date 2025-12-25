import { STORAGE_KEYS } from '../constants';

export const saveSession = (token, user) => {
  try {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    console.log('[AUTH] Session saved');
  } catch (error) {
    console.error('[AUTH] Failed to save session:', error);
  }
};

export const getCurrentUser = () => {
  try {
    const userJson = localStorage.getItem(STORAGE_KEYS.USER);
    return userJson ? JSON.parse(userJson) : null;
  } catch (error) {
    console.error('[AUTH] Failed to parse user data:', error);
    return null;
  }
};

export const getToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  } catch (error) {
    console.error('[AUTH] Failed to get token:', error);
    return null;
  }
};

export const isAuthenticated = () => {
  const token = getToken();
  const user = getCurrentUser();
  return !!(token && user);
};

export const clearSession = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
    console.log('[AUTH] Session cleared');
  } catch (error) {
    console.error('[AUTH] Failed to clear session:', error);
  }
};