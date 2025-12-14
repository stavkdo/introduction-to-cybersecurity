import { useState } from 'react';
import { login } from '../api';

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);

    if (result.success) {
      localStorage.setItem('token', result.data.token);
      localStorage.setItem('user', JSON.stringify(result.data.user));
      onLoginSuccess(result.data.user);
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  const styles = {
    card: {
      backgroundColor: 'white',
      padding: '40px',
      borderRadius: '10px',
      boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
      maxWidth: '400px',
      margin: '50px auto'
    },
    input: {
      width: '100%',
      padding: '12px',
      margin: '10px 0',
      border: '1px solid #ddd',
      borderRadius: '5px',
      fontSize: '14px',
      boxSizing: 'border-box'
    },
    button: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#3498db',
      color: 'white',
      border: 'none',
      borderRadius: '5px',
      cursor: loading ? 'not-allowed' : 'pointer',
      fontSize: '16px',
      fontWeight: 'bold',
      marginTop: '10px',
      opacity: loading ? 0.6 : 1
    },
    error: {
      color: '#e74c3c',
      padding: '12px',
      backgroundColor: '#fadbd8',
      borderRadius: '5px',
      marginTop: '15px',
      fontSize: '14px'
    }
  };

  return (
    <div style={styles.card}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Login</h2>
      
      <form onSubmit={handleSubmit}>
        <input
          style={styles.input}
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          required
        />
        
        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
        
        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      {error && <div style={styles.error}>{error}</div>}
    </div>
  );
}

export default LoginForm;