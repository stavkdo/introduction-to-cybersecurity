import { useState, useEffect } from 'react';
import { getStats } from '../api';

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

  const styles = {
    container: {
      maxWidth: '1000px',
      margin: '0 auto',
      padding: '20px'
    },
    welcomeBox: {
      backgroundColor: '#d4edda',
      color: '#155724',
      padding: '15px',
      borderRadius: '5px',
      marginBottom: '30px',
      border: '1px solid #c3e6cb'
    },
    statsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '20px'
    },
    statCard: {
      backgroundColor: 'white',
      padding: '30px',
      borderRadius: '10px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      textAlign: 'center'
    },
    statTitle: {
      color: '#7f8c8d',
      fontSize: '14px',
      marginBottom: '10px',
      textTransform: 'uppercase',
      letterSpacing: '1px'
    },
    statValue: {
      fontSize: '48px',
      fontWeight: 'bold',
      margin: 0
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', marginTop: '100px', fontSize: '18px' }}>
        Loading...
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h1>Dashboard</h1>
      
      {user && (
        <div style={styles.welcomeBox}>
          <strong>Logged in as:</strong> {user.username} 
          {' '}(Password Strength: <strong>{user.password_strength}</strong>)
        </div>
      )}
      
      {stats && (
        <div style={styles.statsGrid}>
          <div style={styles.statCard}>
            <div style={styles.statTitle}>Total Attempts</div>
            <p style={{ ...styles.statValue, color: '#34495e' }}>
              {stats.total_attempts}
            </p>
          </div>
          
          <div style={styles.statCard}>
            <div style={styles.statTitle}>Successful</div>
            <p style={{ ...styles.statValue, color: '#27ae60' }}>
              {stats.successful}
            </p>
          </div>
          
          <div style={styles.statCard}>
            <div style={styles.statTitle}>Failed</div>
            <p style={{ ...styles.statValue, color: '#e74c3c' }}>
              {stats.failed}
            </p>
          </div>
          
          <div style={styles.statCard}>
            <div style={styles.statTitle}>Success Rate</div>
            <p style={{ ...styles.statValue, color: '#3498db' }}>
              {stats.success_rate}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;