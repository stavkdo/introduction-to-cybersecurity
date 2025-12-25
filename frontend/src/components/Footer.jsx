import { Box, Container, Typography, Divider } from '@mui/material';
import { PROJECT, STUDENTS } from '../constants';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        bgcolor: 'primary.main',
        color: 'var(--text-white)',
        py: 4,
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center' }}>       
          <Typography variant="caption" sx={{ color: 'var(--text-white-disabled)', mb: 1, display: 'block' }}>
            DEVELOPED BY
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 3, justifyContent: 'center', flexWrap: 'wrap', mb: 2 }}>
            {STUDENTS.map((student) => (
              <Box
                key={student.id}
                sx={{
                  p: 1.5,
                  bgcolor: 'var(--hover-overlay)',
                  borderRadius: 1,
                  borderColor: 'secondary.main',
                  transition: 'all 0.3s',
                  '&:hover': {
                    bgcolor: 'var(--hover-overlay-dark)',
                    transform: 'translateY(-2px)',
                  }
                }}
              >
                <Typography variant="body2" fontWeight="600">
                  {student.name}
                </Typography>
                <Typography variant="caption" sx={{ color: 'var(--text-white-secondary)', fontFamily: 'monospace' }}>
                  ID: {student.id}
                </Typography>
              </Box>
            ))}
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;