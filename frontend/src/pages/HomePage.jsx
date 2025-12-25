import { Box, Container, Paper, Typography, Button } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import LoginIcon from '@mui/icons-material/Login';
import { TEXT, PROJECT, ROUTES } from '../constants';

const HomePage = ({ onNavigate }) => {
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
      <Container maxWidth="md">
        <Paper elevation={3} sx={{ p: 6, textAlign: 'center' }}>
          <HomeIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          
          <Typography variant="h3" component="h1" gutterBottom color="primary">
            {TEXT.PROJECT_TITLE}
          </Typography>
          
          <Typography variant="h6" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
            {TEXT.PROJECT_SUBTITLE}
          </Typography>
          
          <Typography variant="body1" color="text.secondary" paragraph sx={{ mb: 4 }}>
            {TEXT.HOME_DESCRIPTION}
          </Typography>
          
          <Box
            sx={{
              p: 2,
              bgcolor: 'var(--bg-light)',
              borderRadius: 1,
              mb: 4,
            }}
          >
            <Typography variant="body2" color="text.secondary">
              <strong>{TEXT.HOME_GROUP_SEED_LABEL}:</strong> {PROJECT.GROUP_SEED}
            </Typography>
          </Box>
          
          <Button
            variant="contained"
            color="primary"
            size="large"
            startIcon={<LoginIcon />}
            onClick={() => onNavigate(ROUTES.LOGIN)}
            sx={{ px: 4 }}
          >
            {TEXT.HOME_CTA}
          </Button>
        </Paper>
      </Container>
    </Box>
  );
};

export default HomePage;