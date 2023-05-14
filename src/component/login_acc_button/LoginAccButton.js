import React from 'react';
import LoginButton from './LoginButton';
import AccountButton from './AccountButton';
import PropTypes from 'prop-types';

function LoginAccButton({ token, setToken }) {

  if (!token) {
    return <LoginButton />;
  } else {
    return <AccountButton setToken={setToken}/>;
  }
}

LoginAccButton.propTypes = {
  token: PropTypes.string.isRequired,
  setToken: PropTypes.func.isRequired
}

export default LoginAccButton;
