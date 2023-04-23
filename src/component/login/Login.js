import React, { useState }from 'react';
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
      <h1>You need to log in first</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Login</button>
        </div>
        <div>
          <p>Don't have an account? </p>
          <a href="/register">Register</a>
        </div>
      </form>
    </div>


  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
}

export default Login;
