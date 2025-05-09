
// src/contexts/CartContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
  // Initialize state from localStorage if available
  const [cartItems, setCartItems] = useState(() => {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });
  
  const [customer, setCustomer] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('CASH');
  const [notes, setNotes] = useState('');
  
  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cartItems));
  }, [cartItems]);
  
  // Add item to cart
  const addItem = (product, quantity = 1) => {
    setCartItems(prevItems => {
      // Check if item already exists in cart
      const existingItemIndex = prevItems.findIndex(item => item.product.id === product.id);
      
      if (existingItemIndex !== -1) {
        // Update quantity if item exists
        const updatedItems = [...prevItems];
        updatedItems[existingItemIndex] = {
          ...updatedItems[existingItemIndex],
          quantity: updatedItems[existingItemIndex].quantity + quantity,
          total: (updatedItems[existingItemIndex].quantity + quantity) * product.price
        };
        return updatedItems;
      } else {
        // Add new item if it doesn't exist
        return [...prevItems, {
          product,
          quantity,
          price: product.price,
          total: quantity * product.price
        }];
      }
    });
  };
  
  // Update item quantity
  const updateItemQuantity = (productId, quantity) => {
    setCartItems(prevItems => {
      return prevItems.map(item => {
        if (item.product.id === productId) {
          return {
            ...item,
            quantity: quantity,
            total: quantity * item.price
          };
        }
        return item;
      });
    });
  };
  
  // Remove item from cart
  const removeItem = (productId) => {
    setCartItems(prevItems => prevItems.filter(item => item.product.id !== productId));
  };
  
  // Clear cart
  const clearCart = () => {
    setCartItems([]);
    setCustomer(null);
    setPaymentMethod('CASH');
    setNotes('');
  };
  
  // Calculate total amount
  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + item.total, 0);
  };
  
  // Get cart summary for API
  const getCartSummary = () => {
    return {
      items: cartItems.map(item => ({
        product: item.product.id,
        quantity: item.quantity,
        price: item.price
      })),
      customer: customer ? customer.id : null,
      total_amount: calculateTotal(),
      payment_method: paymentMethod,
      notes
    };
  };
  
  const value = {
    cartItems,
    customer,
    paymentMethod,
    notes,
    addItem,
    updateItemQuantity,
    removeItem,
    clearCart,
    calculateTotal,
    getCartSummary,
    setCustomer,
    setPaymentMethod,
    setNotes
  };
  
  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};
