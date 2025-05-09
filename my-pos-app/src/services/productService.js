
// src/services/productService.js
import api from '../utils/axiosConfig';

export const getProducts = async () => {
  try {
    const response = await api.get('/api/products/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getProduct = async (id) => {
  try {
    const response = await api.get(`/api/products/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createProduct = async (productData) => {
  try {
    const formData = new FormData();
    
    // Convert product data to FormData for file upload
    Object.keys(productData).forEach(key => {
      formData.append(key, productData[key]);
    });
    
    const response = await api.post('/api/products/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateProduct = async (id, productData) => {
  try {
    const formData = new FormData();
    
    // Convert product data to FormData for file upload
    Object.keys(productData).forEach(key => {
      formData.append(key, productData[key]);
    });
    
    const response = await api.put(`/api/products/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteProduct = async (id) => {
  try {
    const response = await api.delete(`/api/products/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchProducts = async (query) => {
  try {
    const response = await api.get(`/api/products/search/?q=${query}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getProductsByCategory = async (categoryId) => {
  try {
    const response = await api.get(`/api/products/category/${categoryId}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};