import { useState, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Alert,
  Paper,
  Link
} from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import { login } from '../api';
import { saveSession } from '../utils/auth';
import { TEXT } from '../constants';
import CaptchaSection from './CaptchaSection';
import TotpSection from './TotpSection';

const LoginForm = ({ onLoginSuccess, onSwitchToRegister, protectionMode }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [captchaCode, setCaptchaCode] = useState('');
  const [totpCode, setTotpCode] = useState('');

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const [showCaptcha, setShowCaptcha] = useState(false);
  const [showTotp, setShowTotp] = useState(false);

  const [displayedCaptchaImage, setDisplayedCaptchaImage] = useState('');
  const [displayedTotpCode, setDisplayedTotpCode] = useState('');

  // Reset protection-specific state when mode changes
  useEffect(() => {
    console.log('[LOGINFORM] Protection mode changed to:', protectionMode);
    
    // Clear all protection states
    setShowCaptcha(false);
    setShowTotp(false);
    setCaptchaCode('');
    setTotpCode('');
    setDisplayedCaptchaImage('');
    setDisplayedTotpCode('');
    setError('');
  }, [protectionMode]);

  const needsCaptcha = protectionMode === 'CAPTCHA' && showCaptcha;
  const needsTotp = protectionMode === 'TOTP' && showTotp;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const result = await login(username, password, captchaCode, totpCode);

      if (result.success) {
        setSuccess('Login successful! Redirecting...');
        saveSession(result.data.token, result.data.user);
        
        setTimeout(() => {
          onLoginSuccess(result.data.user);
        }, 1000);
        
      } else {
        let errorDetail = result.error;
        
        // Handle error response
        if (typeof errorDetail === 'object' && errorDetail !== null) {
          
          // CAPTCHA required
          if (errorDetail.error === 'captcha_required' && errorDetail.captcha_image) {
            setShowCaptcha(true);
            setDisplayedCaptchaImage(errorDetail.captcha_image);
            setError('CAPTCHA required. Enter the code from the image.');
          } 
          
          // TOTP required
          else if (errorDetail.error === 'totp_required') {
            setShowTotp(true);
            
            if (errorDetail.totp_code) {
              setDisplayedTotpCode(errorDetail.totp_code);
              setError('Two-Factor Authentication required. Code displayed below.');
            } else {
              setError('Two-Factor Authentication required. Click "Show TOTP Code" below.');
            }
          } 
          
          // Other errors
          else {
            setError(errorDetail.message || JSON.stringify(errorDetail));
          }
        } 
        
        // String error messages
        else {
          const errorMsg = String(errorDetail).toLowerCase();
          
          if (errorMsg.includes('captcha')) {
            setShowCaptcha(true);
            setError('CAPTCHA required after multiple failed attempts');
          } else if (errorMsg.includes('totp')) {
            setShowTotp(true);
            setError('Two-Factor Authentication required. Click "Show TOTP Code" below.');
          } else {
            setError(errorDetail);
          }
        }
      }
    } catch (err) {
      console.error('[FORM] Unexpected error:', err);
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 400, width: '100%' }}>
      <Typography variant="h5" component="h2" gutterBottom align="center" sx={{ mb: 3 }}>
        {TEXT.LOGIN_TITLE}
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          fullWidth
          label={TEXT.LOGIN_USERNAME}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
          autoFocus
        />
        
        <TextField
          fullWidth
          type="password"
          label={TEXT.LOGIN_PASSWORD}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        {needsCaptcha && (
          <CaptchaSection
            username={username}
            value={captchaCode}
            onChange={setCaptchaCode}
            disabled={loading}
            initialImage={displayedCaptchaImage}
          />
        )}
        
        {needsTotp && (
          <TotpSection
            username={username}
            value={totpCode}
            onChange={setTotpCode}
            disabled={loading}
            initialCode={displayedTotpCode}
          />
        )}
        
        <Button
          fullWidth
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          disabled={loading}
          startIcon={<LoginIcon />}
          sx={{ mt: 1 }}
        >
          {loading ? TEXT.LOGIN_LOADING : TEXT.LOGIN}
        </Button>
        
        <Typography variant="body2" align="center" sx={{ mt: 2 }}>
          Don't have an account?{' '}
          <Link
            component="button"
            variant="body2"
            onClick={onSwitchToRegister}
            disabled={loading}
            sx={{ cursor: 'pointer' }}
          >
            Register here
          </Link>
        </Typography>
        
        {success && (
          <Alert severity="success" sx={{ mt: 2 }}>
            {success}
          </Alert>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Box>
    </Paper>
  );
};

export default LoginForm;