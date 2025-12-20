
import { useState } from 'react';
import { login } from '../api';
import { saveSession } from '../utils/auth';
import { TEXT } from '../constants';
import '../styles/LoginForm.css';

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

 
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      // Call API
      const result = await login(username, password);

      if (result.success) {
        console.log('Login Success:', result.data);
        setSuccess('Login successful! Redirecting...');
        saveSession(result.data.token, result.data.user);
        
        // Wait for redirect to dashboard
        setTimeout(() => {
          onLoginSuccess(result.data.user);
        }, 1000);
        
      } else {
        console.warn('Login Failed:', result.error);
        setError(result.error);
      }

    } catch (err) {
      console.error('Unexpected error:', err);
      setError('An unexpected error occurred. Please try again.');

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-card">
      <h2 className="login-title">{TEXT.LOGIN_TITLE}</h2>
      
      <form onSubmit={handleSubmit} className="login-form">
        {/* Username Input */}
        <input
          className="login-input"
          type="text"
          placeholder={TEXT.LOGIN_USERNAME}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
          autoFocus
        />
        
        {/* Password Input */}
        <input
          className="login-input"
          type="password"
          placeholder={TEXT.LOGIN_PASSWORD}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        {/* Submit Button */}
        <button 
          className="login-button" 
          type="submit" 
          disabled={loading}
        >
          {loading ? TEXT.LOGIN_LOADING : TEXT.LOGIN_BTN}
        </button>
      </form>
      
      {/* Success Message */}
      {success && (
        <div className="alert alert-success" role="alert">
          {success}
        </div>
      )}
      
      {/* Error Message */}
      {error && (
        <div className="alert alert-error" role="alert">
          {error}
        </div>
      )}
    </div>
  );
}

export default LoginForm;