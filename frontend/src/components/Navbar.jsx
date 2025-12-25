import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LoginIcon from '@mui/icons-material/Login';
import { TEXT, ROUTES } from '../constants';

const Navbar = ({ user, onLogout, onNavigate }) => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ 
            flexGrow: 1, 
            cursor: 'pointer',
            '&:hover': { opacity: 0.8 }
          }}
          onClick={() => onNavigate(ROUTES.HOME)}
        >
          {TEXT.PROJECT_TITLE}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {user ? (
            <>
              <Typography variant="body2" sx={{ color: 'var(--text-white-secondary)' }}>
                {TEXT.WELCOME}, <strong>{user.username}</strong>
              </Typography>
              
              <Button
                color="inherit"
                startIcon={<DashboardIcon />}
                onClick={() => onNavigate(ROUTES.DASHBOARD)}
              >
                {TEXT.NAV_DASHBOARD}
              </Button>
              
              <Button
                color="error"
                variant="contained"
                startIcon={<LogoutIcon />}
                onClick={onLogout}
                size="small"
              >
                {TEXT.LOGOUT}
              </Button>
            </>
          ) : (
            <Button
              color="inherit"
              startIcon={<LoginIcon />}
              onClick={() => onNavigate(ROUTES.LOGIN)}
            >
              {TEXT.LOGIN}
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;