import { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  CircularProgress,
  Card,
  CardContent
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { getStats } from '../api';
import { TEXT } from '../constants';

const DashboardPage = ({ user }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const result = await getStats();
        if (result.success) {
          setStats(result.data);
        }
      } catch (error) {
        console.error('[STATS] Failed to fetch:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }} justifyContent="center">
      <Typography variant="h4" component="h1" gutterBottom color="primary">
        Dashboard
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom sx={{ mb: 4 }}>
        {TEXT.DASHBOARD_LOGGED_IN}: <strong>{user.username}</strong> •{' '}
        {TEXT.DASHBOARD_PASSWORD_STRENGTH}: <strong>{user.password_strength}</strong>
      </Typography>

      {stats && (
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={2}>
              <CardContent sx={{ textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {stats.total_attempts}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {TEXT.STAT_TOTAL}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={2}>
              <CardContent sx={{ textAlign: 'center' }}>
                <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                <Typography variant="h4" color="success.main" fontWeight="bold">
                  {stats.successful}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {TEXT.STAT_SUCCESS}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={2}>
              <CardContent sx={{ textAlign: 'center' }}>
                <CancelIcon sx={{ fontSize: 40, color: 'error.main', mb: 1 }} />
                <Typography variant="h4" color="error.main" fontWeight="bold">
                  {stats.failed}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {TEXT.STAT_FAILED}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={2}>
              <CardContent sx={{ textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h4" color="primary.main" fontWeight="bold">
                  {stats.success_rate}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {TEXT.STAT_RATE}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  );
};

export default DashboardPage;