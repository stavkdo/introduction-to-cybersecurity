import { useState } from 'react';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';

function LoginPage({ onLoginSuccess }) {
  const [showRegister, setShowRegister] = useState(false);

  return (
    <div className="login-page">
      {showRegister ? (
        <RegisterForm 
          onRegisterSuccess={() => setShowRegister(false)}
          onSwitchToLogin={() => setShowRegister(false)}
        />
      ) : (
        <LoginForm 
          onLoginSuccess={onLoginSuccess}
          onSwitchToRegister={() => setShowRegister(true)}
        />
      )}
    </div>
  );
}

export default LoginPage;