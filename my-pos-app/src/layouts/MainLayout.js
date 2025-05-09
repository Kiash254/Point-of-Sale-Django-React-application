
// src/layouts/MainLayout.js
import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Nav, Navbar, Button, Dropdown } from 'react-bootstrap';
import { FaHome, FaShoppingCart, FaBoxes, FaListAlt, FaUsers, FaReceipt, FaUser, FaSignOutAlt, FaBars } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';

const MainLayout = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  return (
    <div className="d-flex">
      {/* Sidebar */}
      <div className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`} style={{ width: sidebarCollapsed ? '80px' : '250px' }}>
        <div className="p-3 d-flex align-items-center justify-content-between">
          {!sidebarCollapsed && <h3 className="m-0">POS System</h3>}
          <Button variant="link" className="text-white p-0" onClick={toggleSidebar}>
            <FaBars />
          </Button>
        </div>
        
        <Nav className="flex-column mt-3">
          <Nav.Link as={Link} to="/app/dashboard" className={location.pathname === '/app/dashboard' ? 'active' : ''}>
            <FaHome className="me-2" /> {!sidebarCollapsed && 'Dashboard'}
          </Nav.Link>
          
          <Nav.Link as={Link} to="/app/pos" className={location.pathname === '/app/pos' ? 'active' : ''}>
            <FaShoppingCart className="me-2" /> {!sidebarCollapsed && 'Point of Sale'}
          </Nav.Link>
          
          <Nav.Link as={Link} to="/app/products" className={location.pathname === '/app/products' ? 'active' : ''}>
            <FaBoxes className="me-2" /> {!sidebarCollapsed && 'Products'}
          </Nav.Link>
          
          <Nav.Link as={Link} to="/app/categories" className={location.pathname === '/app/categories' ? 'active' : ''}>
            <FaListAlt className="me-2" /> {!sidebarCollapsed && 'Categories'}
          </Nav.Link>
          
          <Nav.Link as={Link} to="/app/customers" className={location.pathname === '/app/customers' ? 'active' : ''}>
            <FaUsers className="me-2" /> {!sidebarCollapsed && 'Customers'}
          </Nav.Link>
          
          <Nav.Link as={Link} to="/app/sales" className={location.pathname === '/app/sales' ? 'active' : ''}>
            <FaReceipt className="me-2" /> {!sidebarCollapsed && 'Sales'}
          </Nav.Link>
        </Nav>
      </div>
      
      {/* Main content */}
      <div className="content w-100" style={{ marginLeft: sidebarCollapsed ? '80px' : '250px' }}>
        {/* Top navbar */}
        <Navbar bg="white" className="mb-4 shadow-sm">
          <Container fluid>
            <Navbar.Brand href="/app/dashboard">POS System</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Dropdown align="end">
                <Dropdown.Toggle variant="light" id="dropdown-user">
                  <FaUser className="me-2" />
                  {user?.username}
                </Dropdown.Toggle>
                
                <Dropdown.Menu>
                  <Dropdown.Item as={Link} to="/app/profile">
                    <FaUser className="me-2" /> Profile
                  </Dropdown.Item>
                  <Dropdown.Divider />
                  <Dropdown.Item onClick={handleLogout}>
                    <FaSignOutAlt className="me-2" /> Logout
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        
        {/* Page content */}
        <Container fluid>
          <Outlet />
        </Container>
        
        {/* Footer */}
        <footer className="mt-5 p-3 text-center">
          <p className="mb-0 text-muted">
            &copy; {new Date().getFullYear()} POS System. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
};

export default MainLayout;