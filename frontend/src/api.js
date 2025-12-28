import axios from 'axios';

import { STORAGE_KEYS, API_BASE_URL } from './constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const handleApiSuccess = (data) => ({
  success: true,
  data,
});

const handleApiError = (error) => ({
  success: false,
  error: error.response?.data?.detail || error.message || 'An error occurred',
  errorData: error.response?.data,  
});


export const register = async (username, password, passwordStrength) => {
  try {
    const { data } = await api.post('/register', {
      username,
      password,
      password_strength: passwordStrength,
    });
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error);
  }
};


export const login = async (username, password, captcha_code = null, totp_code = null) => {
  console.log('[API LOGIN] Called with:', { username, password: '***', captcha_code, totp_code });
  try {
    const endpoint = totp_code ? '/login_totp' : '/login';
    
    const payload = {
      username,
      password,
      captcha_code 
    };
    
    if (totp_code) {
      payload.totp_code = totp_code;
    }
    
    const { data } = await api.post(endpoint, payload);
    return handleApiSuccess(data);
    
  } catch (error) {
    return handleApiError(error);
  }
};


export const getTotpCode = async (username, groupSeed) => {
  try {
    const { data } = await api.get('/get_totp', {
      params: { username, group_seed: groupSeed }
    });
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error);
  }
};


export const getStats = async () => {
  try {
    const { data } = await api.get('/stats');
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error);
  }
};

export const getUsers = async () => {
  try {
    const { data } = await api.get('/users');
    return handleApiSuccess(data);
  } catch (error) {
    return handleApiError(error);
  }
};