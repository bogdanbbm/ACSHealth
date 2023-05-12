import React, { useState } from 'react';
import PropTypes from "prop-types";
import axios from "axios";
import './Login.css';
import { useNavigate } from "react-router-dom";

async function loginUser(credentials) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.post(apiURL + '/login', credentials, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response)
    .catch(error => error.response);
}

function Login({ setToken }) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    const response = await loginUser({
      username,
      password
    });

    if (!response) {
      setError('An error occurred. Please try again later.');
      console.log('Unable to connect to the server.');
      navigate('/');
      return;
    }

    if (response.status === 200) {
      const token = response.data.token;
      setToken(token);
      navigate(-1);
    } else if (response.status === 400) {
      setError(response.data.message);
    } else {
      setError('An error occurred. Please try again later.');
      console.log(response)
    }

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
            {error && <p className="err">{error}</p>}
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
