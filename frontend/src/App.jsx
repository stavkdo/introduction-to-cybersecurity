import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import Footer from './components/Footer';
import { ROUTES } from './constants';
import { getCurrentUser, clearSession, isAuthenticated } from './utils/auth'; 

function App() {
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
    <div className="app">
      <Navbar 
        user={user} 
        onLogout={handleLogout}  
        onNavigate={handleNavigate}
      />
      
      <main className="app-content">
        {renderPage()}
      </main>
      <Footer />
    </div>
  );
}

export default App;