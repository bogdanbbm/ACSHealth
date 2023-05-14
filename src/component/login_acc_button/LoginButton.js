import { Link } from 'react-router-dom';
import React from 'react';
import './LoginAccButton.css';

function LoginButton({ token, setToken }) {
  return (
    <div className="login-button">
      <Link to="/login">Login</Link>
    </div>
  );
}

export default LoginButton;
