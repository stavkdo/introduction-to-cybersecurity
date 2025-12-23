import { useState } from 'react';
import { register } from '../api';
import '../styles/RegisterForm.css';

function RegisterForm({ onRegisterSuccess, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordStrength, setPasswordStrength] = useState('medium');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // length limit for now not enforced
    // if (password.length < 6) {
    //   setError('Password must be at least 6 characters');
    //   return;
    // }

    setLoading(true);

    try {
      const result = await register(username, password, passwordStrength);

      if (result.success) {
        setSuccess('Registration successful! Redirecting to login...');
        
        setTimeout(() => {
          onRegisterSuccess();
        }, 1500);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-card">
      <h2 className="register-title">Register</h2>
      
      <form onSubmit={handleSubmit} className="register-form">
        <input
          className="form-input"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
          autoFocus
        />
        
        <input
          className="form-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        <input
          className="form-input"
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        <div className="strength-selector">
          <label className="strength-label">Password Strength:</label>
          <select 
            className="strength-select"
            value={passwordStrength}
            onChange={(e) => setPasswordStrength(e.target.value)}
            disabled={loading}
          >
            <option value="weak">Weak</option>
            <option value="medium">Medium</option>
            <option value="strong">Strong</option>
          </select>
        </div>
        
        <button 
          className="btn btn-primary" 
          type="submit" 
          disabled={loading}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      
      <div className="switch-auth">
        Already have an account?{' '}
        <button 
          className="link-button"
          onClick={onSwitchToLogin}
          disabled={loading}
          type="button"
        >
          Login here
        </button>
      </div>
      
      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}
      
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}
    </div>
  );
}

export default RegisterForm;