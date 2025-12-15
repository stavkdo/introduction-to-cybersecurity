import LoginForm from '../components/LoginForm';

function LoginPage({ onLoginSuccess }) {
  return (
    <div className="login-page">
      <LoginForm onLoginSuccess={onLoginSuccess} />
    </div>
  );
}

export default LoginPage;