import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import { ROUTES, STORAGE_KEYS } from './constants';

function App() {
  const [currentPage, setCurrentPage] = useState(ROUTES.HOME);
  const [user, setUser] = useState(null);

  // Load user from storage on mount
  useEffect(() => {
    const savedUser = getStoredUser();
    if (savedUser) {
      setUser(savedUser);
      setCurrentPage(ROUTES.DASHBOARD);
    }
  }, []);

  // Helper: Get user from localStorage (DRY)
  const getStoredUser = () => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    const userJson = localStorage.getItem(STORAGE_KEYS.USER);
    return token && userJson ? JSON.parse(userJson) : null;
  };

  // Helper: Clear storage (DRY)
  const clearStorage = () => {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  };

  // Handlers
  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setCurrentPage(ROUTES.DASHBOARD);
  };

  const handleLogout = () => {
    clearStorage();
    setUser(null);
    setCurrentPage(ROUTES.HOME);
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  // Render current page (DRY)
  const renderPage = () => {
    const pages = {
      [ROUTES.HOME]: <HomePage onNavigate={handleNavigate} />,
      [ROUTES.LOGIN]: <LoginPage onLoginSuccess={handleLoginSuccess} />,
      [ROUTES.DASHBOARD]: user && <DashboardPage user={user} />,
    };
    return pages[currentPage];
  };

  return (
    <div style={{ backgroundColor: '#ecf0f1', minHeight: '100vh' }}>
      <Navbar 
        user={user} 
        onLogout={handleLogout}
        onNavigate={handleNavigate}
      />
      {renderPage()}
    </div>
  );
}

export default App;