
// src/services/authService.js
import api from '../utils/axiosConfig';

export const login = async (username, password) => {
  try {
    const response = await api.post('/api/token/', { username, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/api/register/', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getUserProfile = async () => {
  try {
    const response = await api.get('/api/profile/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateUserProfile = async (userData) => {
  try {
    const response = await api.put('/api/profile/', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};