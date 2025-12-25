import { useState } from 'react';
import { Box, TextField, Button, Typography, Alert } from '@mui/material';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import { getTotpCode } from '../api';
import { PROJECT } from '../constants';

const TotpSection = ({ username, value, onChange, disabled }) => {
  const [displayedCode, setDisplayedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleShowCode = async () => {
    if (!username) {
      setError('Please enter username first');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const result = await getTotpCode(username, PROJECT.GROUP_SEED);
      if (result.success) {
        const code = result.data.totp_code;
        setDisplayedCode(code);
        onChange(code);
      } else {
        setError('User does not have TOTP enabled');
      }
    } catch (err) {
      setError('Failed to get TOTP code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: 'var(--totp-bg)',
        borderRadius: 1,
        border: '2px solid var(--totp-border)',
      }}
    >
      <Typography variant="subtitle2" fontWeight="600" color="var(--totp-text)" gutterBottom>
        Two-Factor Authentication (TOTP)
      </Typography>
      
      {displayedCode && (
        <Box
          sx={{
            my: 2,
            p: 2,
            bgcolor: 'var(--bg-white)',
            borderRadius: 1,
            textAlign: 'center',
          }}
        >
          <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
            Your TOTP code:
          </Typography>
          <Typography
            variant="h3"
            sx={{
              fontFamily: 'monospace',
              letterSpacing: 8,
              fontWeight: 'bold',
              border: '2px solid var(--totp-border)',
              p: 1,
              borderRadius: 1,
              bgcolor: 'var(--totp-code-bg)',
            }}
          >
            {displayedCode}
          </Typography>
        </Box>
      )}
      
      <TextField
        fullWidth
        label="Enter 6-digit TOTP code"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled || loading}
        required
        inputProps={{ maxLength: 6 }}
        sx={{ mt: 2, bgcolor: 'var(--bg-white)' }}
      />
      
      <Button
        fullWidth
        variant="contained"
        color="info"
        onClick={handleShowCode}
        disabled={disabled || loading || !username}
        startIcon={<VpnKeyIcon />}
        sx={{ mt: 2 }}
      >
        {loading ? 'Loading...' : 'Show TOTP Code'}
      </Button>
      
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default TotpSection;