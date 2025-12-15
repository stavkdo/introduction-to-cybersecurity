import { useState, useEffect } from 'react';
import { getStats } from '../api';
import { TEXT } from '../constants';
import '../styles/Dashboard.css';

function DashboardPage({ user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    const result = await getStats();
    if (result.success) {
      setStats(result.data);
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="dashboard-loading">{TEXT.LOADING}</div>;
  }

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">{TEXT.NAV_DASHBOARD}</h1>
      
      {user && (
        <div className="dashboard-welcome">
          <strong>{TEXT.DASHBOARD_LOGGED_IN}:</strong> {user.username}
          {' '}({TEXT.DASHBOARD_PASSWORD_STRENGTH}: <strong>{user.password_strength}</strong>)
        </div>
      )}
      
      {stats && (
        <div className="stats-grid">
          <StatCard 
            title={TEXT.STAT_TOTAL} 
            value={stats.total_attempts} 
            colorClass="total"
          />
          <StatCard 
            title={TEXT.STAT_SUCCESS} 
            value={stats.successful} 
            colorClass="success"
          />
          <StatCard 
            title={TEXT.STAT_FAILED} 
            value={stats.failed} 
            colorClass="error"
          />
          <StatCard 
            title={TEXT.STAT_RATE} 
            value={`${stats.success_rate}%`} 
            colorClass="info"
          />
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, colorClass }) {
  return (
    <div className="stat-card">
      <div className="stat-title">{title}</div>
      <p className={`stat-value ${colorClass}`}>{value}</p>
    </div>
  );
}

export default DashboardPage;