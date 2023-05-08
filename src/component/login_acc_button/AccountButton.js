import React from 'react';
import useToken from '../../hooks/useToken';
import { useNavigate } from "react-router-dom";

function AccountButton() {
  const {setToken} = useToken();
  const navigate = useNavigate();
  const handleClick = () => {
    setToken(null);
    navigate('/');
  }

  return (
    <div>
      <button onClick={handleClick}>Log out</button>
    </div>
  );
}

export default AccountButton;