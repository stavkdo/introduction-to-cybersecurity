import { useState } from 'react';
import { login, getCaptchaToken } from '../api';
import { saveSession } from '../utils/auth';
import { TEXT, PROJECT } from '../constants';
import '../styles/LoginForm.css';

function LoginForm({ onLoginSuccess, onSwitchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [totpCode, setTotpCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [captchaRequired, setCaptchaRequired] = useState(false);
  const [totpRequired, setTotpRequired] = useState(false);
  const [captchaToken, setCaptchaToken] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const result = await login(username, password, captchaToken, totpCode);

      if (result.success) {
        setSuccess('Login successful! Redirecting...');
        saveSession(result.data.token, result.data.user);
        
        setTimeout(() => {
          onLoginSuccess(result.data.user);
        }, 1000);
        
      } else {
        const errorMsg = result.error.toLowerCase();
        
        if (errorMsg.includes('captcha')) {
          setCaptchaRequired(true);
          setError('CAPTCHA verification required');
        } else if (errorMsg.includes('totp')) {
          setTotpRequired(true);
          setError('TOTP code required');
        } else {
          setError(result.error);
        }
      }

    } catch (err) {
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGetCaptcha = async () => {
    setLoading(true);
    try {
      const result = await getCaptchaToken(PROJECT.GROUP_SEED);
      if (result.success) {
        setCaptchaToken(result.data.captcha_token);
        setSuccess('CAPTCHA token received! Now click Login.');
        setError('');
      } else {
        setError('Failed to get CAPTCHA token');
      }
    } catch (err) {
      setError('Failed to get CAPTCHA token');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-card">
      <h2 className="login-title">{TEXT.LOGIN_TITLE}</h2>
      
      <form onSubmit={handleSubmit} className="login-form">
        <Input
          type="text"
          placeholder={TEXT.LOGIN_USERNAME}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
          autoFocus
        />
        
        <Input
          type="password"
          placeholder={TEXT.LOGIN_PASSWORD}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        {totpRequired && (
          <Input
            type="text"
            placeholder="TOTP Code (6 digits)"
            value={totpCode}
            onChange={(e) => setTotpCode(e.target.value)}
            disabled={loading}
            required
          />
        )}
        
        <Button type="submit" loading={loading}>
          {TEXT.LOGIN}
        </Button>
      </form>
      
      {captchaRequired && (
        <div className="captcha-section">
          <p className="captcha-text">CAPTCHA verification required</p>
          <Button variant="warning" onClick={handleGetCaptcha} disabled={loading}>
            Get CAPTCHA Token
          </Button>
          {captchaToken && (
            <div className="captcha-token">
              <strong>Token:</strong> {captchaToken.substring(0, 16)}...
            </div>
          )}
        </div>
      )}
      
      <div className="switch-auth">
        Don't have an account?{' '}
        <button 
          className="link-button"
          onClick={onSwitchToRegister}
          disabled={loading}
        >
          Register here
        </button>
      </div>
      
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />
    </div>
  );
}

export default LoginForm;