import { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import { ROUTES } from './constants';
import { getCurrentUser, clearSession, isAuthenticated } from './utils/auth';

const App = () => {
  const [currentPage, setCurrentPage] = useState(ROUTES.HOME);
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (isAuthenticated()) {
      const savedUser = getCurrentUser();
      setUser(savedUser);
      setCurrentPage(ROUTES.DASHBOARD);
      console.log('[APP] Restored session:', savedUser.username);
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setCurrentPage(ROUTES.DASHBOARD);
    console.log('[APP] User logged in:', userData.username);
  };

  const handleLogout = () => {
    clearSession();
    setUser(null);
    setCurrentPage(ROUTES.HOME);
    console.log('[APP] User logged out');
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
    console.log('[APP] Navigated to:', page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case ROUTES.HOME:
        return <HomePage onNavigate={handleNavigate} />;
      
      case ROUTES.LOGIN:
        return <LoginPage onLoginSuccess={handleLoginSuccess} />;
      
      case ROUTES.DASHBOARD:
        return user ? (
          <DashboardPage user={user} />
        ) : (
          <LoginPage onLoginSuccess={handleLoginSuccess} />
        );
      
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar 
        user={user} 
        onLogout={handleLogout}
        onNavigate={handleNavigate}
      />
      
      <Box component="main" sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {renderPage()}
      </Box>
      
      <Footer />
    </Box>
  );
};

export default App;