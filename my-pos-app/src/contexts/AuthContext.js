
// src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { API_URL } from '../utils/constants';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  
  const navigate = useNavigate ? useNavigate() : null;
  
  // Set axios defaults for auth
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);
  
  // Load user data from token
  useEffect(() => {
    const loadUser = async () => {
      try {
        if (token) {
          // Check if token is expired
          const decoded = jwt_decode(token);
          const currentTime = Date.now() / 1000;
          
          if (decoded.exp < currentTime) {
            logout();
            return;
          }
          
          // Get user profile
          const res = await axios.get(`${API_URL}/api/profile/`);
          setUser(res.data);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Auth error:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };
    
    loadUser();
  }, [token]);
  
  const login = async (username, password) => {
    try {
      const res = await axios.post(`${API_URL}/api/token/`, {
        username,
        password
      });
      
      const { access, refresh } = res.data;
      
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      setToken(access);
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };
  
  const register = async (userData) => {
    try {
      await axios.post(`${API_URL}/api/register/`, userData);
      return true;
    } catch (error) {
      console.error('Register error:', error);
      return false;
    }
  };
  
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    
    if (navigate) {
      navigate('/login');
    }
  };
  
  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (!refreshToken) {
        logout();
        return false;
      }
      
      const res = await axios.post(`${API_URL}/api/token/refresh/`, {
        refresh: refreshToken
      });
      
      const { access } = res.data;
      
      localStorage.setItem('token', access);
      setToken(access);
      
      return true;
    } catch (error) {
      console.error('Refresh token error:', error);
      logout();
      return false;
    }
  };
  
  const value = {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    refreshToken
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
