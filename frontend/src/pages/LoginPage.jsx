import LoginForm from '../components/LoginForm';

function LoginPage({ onLoginSuccess }) {
  return <LoginForm onLoginSuccess={onLoginSuccess} />;
}

export default LoginPage;