
// src/services/customerService.js
import api from '../utils/axiosConfig';

export const getCustomers = async () => {
  try {
    const response = await api.get('/api/customers/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCustomer = async (id) => {
  try {
    const response = await api.get(`/api/customers/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createCustomer = async (customerData) => {
  try {
    const response = await api.post('/api/customers/', customerData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateCustomer = async (id, customerData) => {
  try {
    const response = await api.put(`/api/customers/${id}/`, customerData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteCustomer = async (id) => {
  try {
    const response = await api.delete(`/api/customers/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchCustomers = async (query) => {
  try {
    const response = await api.get(`/api/customers/search/?q=${query}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// src/services/saleService.js
import api from '../utils/axiosConfig';

export const getSales = async (page = 1, filters = {}) => {
  try {
    let queryParams = `?page=${page}`;
    
    if (filters.startDate && filters.endDate) {
      queryParams += `&start_date=${filters.startDate}&end_date=${filters.endDate}`;
    }
    
    if (filters.status) {
      queryParams += `&status=${filters.status}`;
    }
    
    const response = await api.get(`/api/sales/${queryParams}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getSale = async (id) => {
  try {
    const response = await api.get(`/api/sales/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createSale = async (saleData) => {
  try {
    const response = await api.post('/api/sales/create/', saleData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getDashboardStats = async () => {
  try {
    const response = await api.get('/api/dashboard/stats/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getDailySales = async () => {
  try {
    const response = await api.get('/api/dashboard/sales/daily/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getWeeklySales = async () => {
  try {
    const response = await api.get('/api/dashboard/sales/weekly/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getMonthlySales = async () => {
  try {
    const response = await api.get('/api/dashboard/sales/monthly/');
    return response.data;
  } catch (error) {
    throw error;
  }
};
