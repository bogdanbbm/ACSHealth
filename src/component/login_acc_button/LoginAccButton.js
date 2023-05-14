import React from 'react';
import LoginButton from './LoginButton';
import AccountButton from './AccountButton';
import useToken from '../../hooks/useToken';

function LoginAccButton() {
  const {token} = useToken();

  if (!token) {
    return <LoginButton />;
  } else {
    return <AccountButton />;
  }
}

export default LoginAccButton;