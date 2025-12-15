import { TEXT, PROJECT, ROUTES } from '../constants';
import '../styles/HomePage.css';

function HomePage({ onNavigate }) {
  return (
    <div className="home-container">
      <div className="home-card">
        <h1 className="home-title">{TEXT.PROJECT_TITLE}</h1>
        <p className="home-subtitle">{TEXT.PROJECT_SUBTITLE}</p>
        
        <div className="home-description">
          <p>{TEXT.HOME_DESCRIPTION}</p>
          <p className="home-group-seed">
            <strong>{TEXT.HOME_GROUP_SEED_LABEL}:</strong> {PROJECT.GROUP_SEED}
          </p>
        </div>
        
        <button 
          className="home-button"
          onClick={() => onNavigate(ROUTES.LOGIN)}
        >
          {TEXT.HOME_CTA}
        </button>
      </div>
    </div>
  );
}

export default HomePage;