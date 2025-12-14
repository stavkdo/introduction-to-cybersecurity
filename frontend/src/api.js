import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  try {
    const { data } = await api.post('/login', { username, password });
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Login failed'
    };
  }
};

export const getStats = async () => {
  try {
    const { data } = await api.get('/stats');
    return { success: true, data };
  } catch (error) {
    return { success: false, error: 'Failed to load stats' };
  }
};