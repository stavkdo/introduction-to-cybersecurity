import axios from 'axios';
import { API_BASE_URL, STORAGE_KEYS } from './constants';

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const handleApiError = (error, defaultMessage) => {
  let errorMessage = defaultMessage;
  
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    
    if (typeof detail === 'string') {
      errorMessage = detail;
    } else if (detail.message) {
      errorMessage = detail.message;
    }
  }
  
  return {
    success: false,
    error: errorMessage
  };
};

const handleApiSuccess = (data) => ({
  success: true,
  data
});

export const register = async (username, password, password_strength = 'medium') => {
  try {
    const { data } = await api.post('/register', {
      username,
      password,
      password_strength
    });
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error, 'Registration failed');
  }
};

export const login = async (username, password, captcha_token = null, totp_code = null) => {
  try {
    const payload = { username, password };
    if (captcha_token) payload.captcha_token = captcha_token;
    
    const endpoint = totp_code ? '/login_totp' : '/login';
    
    if (totp_code) {
      payload.totp_code = totp_code;
    }
    
    const { data } = await api.post(endpoint, payload);
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error, 'Login failed');
  }
};

export const getStats = async () => {
  try {
    const { data } = await api.get('/stats');
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error, 'Failed to load stats');
  }
};

export const getCaptchaToken = async (groupSeed) => {
  try {
    const { data } = await api.get(`http://localhost:8000/admin/get_captcha_token?group_seed=${groupSeed}`);
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error, 'Failed to get CAPTCHA token');
  }
};