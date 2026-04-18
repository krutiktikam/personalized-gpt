import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add a request interceptor to attach the JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('aura_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only clear token if it's a 401 on a non-login endpoint
    if (error.response && error.response.status === 401 && !error.config.url.endsWith('/token')) {
      localStorage.removeItem('aura_token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export default api;
