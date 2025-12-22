import '../styles/Navbar.css';
import { TEXT, ROUTES } from '../constants';

function Navbar({ user, onLogout, onNavigate }) {
  return (
    <nav className="navbar">
      <h2 
        className="navbar-title" 
        onClick={() => onNavigate(ROUTES.HOME)}
        style={{ cursor: 'pointer' }}
      >
        {TEXT.PROJECT_TITLE}
      </h2>
     
      <div className="navbar-actions">
        {user ? (
          <>
            <span className="navbar-welcome">
              {TEXT.WELCOME}, <strong>{user.username}</strong>
            </span>
            
            <button 
              className="navbar-button" 
              onClick={() => onNavigate(ROUTES.DASHBOARD)}
            >
              {TEXT.NAV_DASHBOARD}
            </button>
            
            <button 
              className="navbar-button navbar-button-logout" 
              onClick={onLogout}  
            >
              {TEXT.LOGOUT}
            </button>
          </>
        ) : (
          <button 
            className="navbar-button" 
            onClick={() => onNavigate(ROUTES.LOGIN)}
          >
            {TEXT.LOGIN}
          </button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;