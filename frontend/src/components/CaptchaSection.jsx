import { useState, useEffect } from 'react';
import { Box, TextField, Button, Typography, Alert } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

const CaptchaSection = ({ username, value, onChange, disabled, initialImage = '' }) => {
  const [captchaImage, setCaptchaImage] = useState(initialImage);
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialImage) {
      console.log('[CAPTCHA] Received new image');
      setCaptchaImage(initialImage);
    }
  }, [initialImage]);

  const handleInputChange = (e) => {
    const newValue = e.target.value.toUpperCase();
    console.log('[CAPTCHA] Input changed to:', `'${newValue}'`);
    onChange(newValue);
  };

  console.log('[CAPTCHA] Render - value:', `'${value}'`, 'hasImage:', !!captchaImage);

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: 'var(--captcha-bg)',
        borderRadius: 1,
        border: '2px solid var(--captcha-border)',
      }}
    >
      <Typography variant="subtitle2" fontWeight="600" color="var(--captcha-text)" gutterBottom>
        🔒 CAPTCHA Verification Required
      </Typography>
      
      {captchaImage && (
        <Box
          sx={{
            my: 2,
            p: 2,
            bgcolor: 'var(--bg-white)',
            borderRadius: 1,
            textAlign: 'center',
          }}
        >
          <Typography variant="caption" color="text.secondary" display="block" gutterBottom fontWeight="600">
            Type the characters you see in the image:
          </Typography>
          <Box
            component="img"
            src={`data:image/png;base64,${captchaImage}`}
            alt="CAPTCHA"
            sx={{
              maxWidth: '100%',
              height: 'auto',
              border: '1px solid var(--captcha-border)',
              borderRadius: 1,
              my: 1,
            }}
          />
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
            ℹ️ Enter the code exactly as shown
          </Typography>
        </Box>
      )}
      
      <TextField
        fullWidth
        label="Enter CAPTCHA code"
        placeholder="Type what you see"
        value={value}
        onChange={handleInputChange}
        disabled={disabled}
        required
        sx={{ mt: 2, bgcolor: 'var(--bg-white)' }}
        helperText={value ? `You entered: ${value}` : 'Type the characters from the image above'}
      />
      
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default CaptchaSection;