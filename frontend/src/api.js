import axios from 'axios';
import { API_BASE_URL, STORAGE_KEYS } from './constants';

const api = axios.create({
  baseURL: API_BASE_URL
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Generic error handler (DRY)
const handleApiError = (error, defaultMessage) => ({
  success: false,
  error: error.response?.data?.detail || defaultMessage
});

// Generic success handler (DRY)
const handleApiSuccess = (data) => ({
  success: true,
  data
});

// API Methods
export const login = async (username, password) => {
  try {
    const { data } = await api.post('/login', { username, password });
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