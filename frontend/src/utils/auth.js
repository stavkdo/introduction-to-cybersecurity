
import { STORAGE_KEYS } from '../constants';


export function saveSession(token, user) {
  try {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    console.log('Session saved');
  } catch (error) {
    console.error('Failed to save session:', error);
  }
}

export function getCurrentUser() {
  try {
    const userJson = localStorage.getItem(STORAGE_KEYS.USER);
    return userJson ? JSON.parse(userJson) : null;
  } catch (error) {
    console.error('Failed to parse user data:', error);
    return null;
  }
}

export function getToken() {
  return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

export function isAuthenticated() {
  const token = getToken();
  const user = getCurrentUser();
  return !!(token && user);
}

export function clearSession() {
  try {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
    console.log('Session cleared');
  } catch (error) {
    console.error('Failed to clear session:', error);
  }
}