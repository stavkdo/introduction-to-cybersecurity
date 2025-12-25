import { useState, useEffect } from 'react';
import { Box, Container, CircularProgress } from '@mui/material';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';
import axios from 'axios';
import { API_BASE_URL } from '../constants';

const LoginPage = ({ onLoginSuccess }) => {
  const [showRegister, setShowRegister] = useState(false);
  const [protectionMode, setProtectionMode] = useState('NONE');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const { data } = await axios.get(`${API_BASE_URL}/config`);
        setProtectionMode(data.protection_mode);
        console.log('[CONFIG] Protection mode:', data.protection_mode);
      } catch (error) {
        console.error('[CONFIG] Failed to fetch config:', error);
        setProtectionMode('NONE');
      } finally {
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: 'calc(100vh - 160px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: 'var(--bg-light)',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 160px)',
        display: 'flex',
        alignItems: 'center',
        bgcolor: 'var(--bg-light)',
        py: 4,
      }}
    >
      <Container maxWidth="sm" sx={{ display: 'flex', justifyContent: 'center' }}>
        {showRegister ? (
          <RegisterForm
            onRegisterSuccess={() => setShowRegister(false)}
            onSwitchToLogin={() => setShowRegister(false)}
          />
        ) : (
          <LoginForm
            onLoginSuccess={onLoginSuccess}
            onSwitchToRegister={() => setShowRegister(true)}
            protectionMode={protectionMode}
          />
        )}
      </Container>
    </Box>
  );
};

export default LoginPage;