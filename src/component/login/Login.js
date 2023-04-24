import React, { useState } from 'react';
import PropTypes from "prop-types";
import axios from "axios";
import './Login.css';

async function loginUser(credentials) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.post(apiURL + '/login', credentials, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.data)
    .catch(error => console.error(error));
}

function Login({ setToken }) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password
    });
    setToken(token);
  }

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-header">Login</div>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <input type="text" id="username" required onChange={e => setUserName(e.target.value)} />
            <label for="username">Username</label>
          </div>
          <div className="field">
            <input type="password" id="password" required onChange={e => setPassword(e.target.value)}/>
            <label for="password">Password</label>
          </div>
          <div className="field">
            <button type="submit">Login</button>
          </div>
          <div className="register-link">
            <p>Don't have an account? </p>
            <a href="/register">Register</a>
          </div>
        </form>
      </div>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
}

export default Login;
