import '../styles/Navbar.css';
import { TEXT, ROUTES } from '../constants';

function Navbar({ user, onLogout, onNavigate }) {
  return (
    <div className="navbar">
      <h2 className="navbar-title" onClick={() => onNavigate(ROUTES.HOME)}>
        {TEXT.PROJECT_TITLE}
      </h2>
      
      <div className="navbar-actions">
        {user ? (
          <>
            <span className="navbar-welcome">
              {TEXT.WELCOME}, {user.username}
            </span>
            <button 
              className="navbar-button" 
              onClick={() => onNavigate(ROUTES.DASHBOARD)}
            >
              {TEXT.NAV_DASHBOARD}
            </button>
            <button className="navbar-button" onClick={onLogout}>
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
    </div>
  );
}

export default Navbar;