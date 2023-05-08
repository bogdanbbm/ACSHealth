// noinspection JSCheckFunctionSignatures

import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

async function registerUser(credentials) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.post(apiURL + '/register', credentials, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response)
    .catch(error => error.response);
}

function Register() {
  const [input, setInput] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
  });

  const [error, setError] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
  });

  const [isMedic, setIsMedic] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const navigate = useNavigate();

  const onInputChange = e => {
    const { name, value } = e.target;
    setInput(prev => ({
      ...prev,
      [name]: value
    }));
    validateInput(e);
  }

  const validateInput = e => {
    let { name, value } = e.target;
    setError(prev => {
      const stateObj = { ...prev, [name]: '' };

      switch (name) {
        case 'username':
          if (!value) {
            stateObj[name] = 'Username is required';
          } else if (value.length < 3) {
            stateObj[name] = 'Username must be at least 3 characters long';
          }
          break;

        case 'password':
          if (!value) {
            stateObj[name] = 'Password is required';
          } else if(!value.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/)) {
            stateObj[name] = 'Password must be at least 8 characters long and contain at least one letter and one number';
          } else if (input.confirmPassword && value !== input.confirmPassword) {
            stateObj['confirmPassword'] = 'Passwords do not match';
          } else {
            stateObj['confirmPassword'] = input.confirmPassword ? '' : error.confirmPassword;
          }
          break;

        case 'confirmPassword':
          if (!value) {
            stateObj[name] = 'Confirm password is required';
          } else if (input.password && value !== input.password) {
            stateObj[name] = 'Passwords do not match';
          }
          break;

        case 'email':
          if (!value) {
            stateObj[name] = 'Email is required';
          } else if (!value.match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
            stateObj[name] = 'Invalid email';
          }
          break;

        default:
          break;
      }

      return stateObj;
    });
  }

  const handleSubmit = async e => {
    e.preventDefault();
    if (Object.values(error).some(err => err)) {
      setSubmitError('All fields must be valid!');
      return;
    }

    setSubmitError('');

    const response = await registerUser({
      email: input.email,
      username: input.username,
      password: input.password,
      isMedic: isMedic
    });

    if (!response) {
      setSubmitError('Something went wrong!');
      return;
    }

    if (response.status === 201) {
      navigate('/register/success');
    } else if (response.status === 409) {
      setSubmitError(response.data.message);
    } else {
      setSubmitError('Something went wrong!');
    }
  }

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-header">Register</div>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <input
              id="username"
              type="text"
              name="username"
              required
              value={input.username}
              onChange={onInputChange}
              onBlur={validateInput} />
            <label for="username">Username</label>
            {error.username && <p className="err">{error.username}</p>}
          </div>
          <div className="field">
            <input
              id="email"
              type="email"
              name="email"
              required
              value={input.email}
              onChange={onInputChange}
              onBlur={validateInput} />
            <label for="email">Email</label>
            {error.email && <p className="err">{error.email}</p>}
          </div>
          <div className="field">
            <input
              id="password"
              type="password"
              name="password"
              required
              value={input.password}
              onChange={onInputChange}
              onBlur={validateInput} />
            <label for="password">Password</label>
            {error.password && <p className="err">{error.password}</p>}
          </div>
          <div className="field">
            <input
              id="confirmPassword"
              type="password"
              name="confirmPassword"
              required
              value={input.confirmPassword}
              onChange={onInputChange}
              onBlur={validateInput} />
            <label for="confirmPassword">Confirm Password</label>
            {error.confirmPassword && <p className="err">{error.confirmPassword}</p>}
          </div>
          <div className="checkbox">
            <p>Are you registering as a medic?</p>
            <input  type="checkbox" onChange={e => setIsMedic(e.target.checked)} />
          </div>
          <div className="field">
            <button type="submit">Register</button>
            {submitError && <p className="err">{submitError}</p>}
          </div>
        </form>
      </div>
    </div>
  );
}

export default Register;
