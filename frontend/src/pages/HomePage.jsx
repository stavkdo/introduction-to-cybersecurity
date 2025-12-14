function HomePage({ onNavigate }) {
  const styles = {
    container: {
      maxWidth: '600px',
      margin: '50px auto',
      textAlign: 'center'
    },
    card: {
      backgroundColor: 'white',
      padding: '40px',
      borderRadius: '10px',
      boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
    },
    title: {
      fontSize: '32px',
      marginBottom: '10px',
      color: '#2c3e50'
    },
    subtitle: {
      color: '#7f8c8d',
      marginBottom: '20px'
    },
    description: {
      lineHeight: '1.6',
      color: '#34495e',
      marginBottom: '30px'
    },
    button: {
      padding: '15px 40px',
      backgroundColor: '#3498db',
      color: 'white',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '16px',
      fontWeight: 'bold'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Password Authentication Research</h1>
        <p style={styles.subtitle}>Security Course 20940</p>
        
        <div style={styles.description}>
          <p>
            This is a research project analyzing password authentication 
            mechanisms and their resilience against common attack vectors.
          </p>
          <p>
            <strong>Group Seed:</strong> 211245440
          </p>
        </div>
        
        <button style={styles.button} onClick={() => onNavigate('login')}>
          Go to Login
        </button>
      </div>
    </div>
  );
}

export default HomePage;