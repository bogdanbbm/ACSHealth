import React from 'react';
import { useNavigate } from "react-router-dom";
import './LoginAccButton.css'
import PropTypes from 'prop-types';

function AccountButton({ setToken }) {
  const navigate = useNavigate();
  const handleClick = () => {
    setToken(null);
    navigate('/');
  }

  return (
    <div className="login-button">
      <button onClick={handleClick}>Log out</button>
    </div>
  );
}

AccountButton.propTypes = {
  setToken: PropTypes.func.isRequired
}

export default AccountButton;
