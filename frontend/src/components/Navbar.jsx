function Navbar({ user, onLogout, onNavigate }) {
  const styles = {
    navbar: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '20px 40px',
      backgroundColor: '#2c3e50',
      color: 'white',
      marginBottom: '30px',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
    },
    title: {
      margin: 0,
      fontSize: '24px',
      cursor: 'pointer'
    },
    button: {
      padding: '10px 20px',
      backgroundColor: '#3498db',
      color: 'white',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '14px',
      marginLeft: '10px'
    },
    welcomeText: {
      marginRight: '20px'
    }
  };

  return (
    <div style={styles.navbar}>
      <h2 style={styles.title} onClick={() => onNavigate('home')}>
        Password Auth Research
      </h2>
      
      <div>
        {user ? (
          <>
            <span style={styles.welcomeText}>Welcome, {user.username}</span>
            <button style={styles.button} onClick={() => onNavigate('dashboard')}>
              Dashboard
            </button>
            <button style={styles.button} onClick={onLogout}>
              Logout
            </button>
          </>
        ) : (
          <button style={styles.button} onClick={() => onNavigate('login')}>
            Login
          </button>
        )}
      </div>
    </div>
  );
}

export default Navbar;