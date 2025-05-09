
// src/services/categoryService.js
import api from '../utils/axiosConfig';

export const getCategories = async () => {
  try {
    const response = await api.get('/api/categories/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCategory = async (id) => {
  try {
    const response = await api.get(`/api/categories/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createCategory = async (categoryData) => {
  try {
    const response = await api.post('/api/categories/', categoryData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateCategory = async (id, categoryData) => {
  try {
    const response = await api.put(`/api/categories/${id}/`, categoryData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteCategory = async (id) => {
  try {
    const response = await api.delete(`/api/categories/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};