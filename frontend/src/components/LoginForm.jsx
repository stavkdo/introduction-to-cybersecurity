import { useState } from 'react';
import { login } from '../api';
import { TEXTS, STORAGE_KEYS } from '../constants/constants';
import '../styles/LoginForm.css';

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);

    if (result.success) {
      localStorage.setItem(STORAGE_KEYS.TOKEN, result.data.token);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(result.data.user));
      onLoginSuccess(result.data.user);
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="login-card">
      <h2 className="login-title">{TEXTS.LOGIN_TITLE}</h2>
      
      <form onSubmit={handleSubmit} className="login-form">
        <input
          className="login-input"
          type="text"
          placeholder={TEXTS.LOGIN_USERNAME_PLACEHOLDER}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
        />
        
        <input
          className="login-input"
          type="password"
          placeholder={TEXTS.LOGIN_PASSWORD_PLACEHOLDER}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        <button className="login-button" type="submit" disabled={loading}>
          {loading ? TEXTS.LOGIN_LOADING : TEXTS.LOGIN_BUTTON}
        </button>
      </form>
      
      {error && <div className="alert alert-error">{error}</div>}
    </div>
  );
}

export default LoginForm;