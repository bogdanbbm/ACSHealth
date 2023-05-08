import React, { useEffect } from 'react';
import useToken from "../../hooks/useToken";
import { useNavigate } from "react-router-dom";

function MedicalData() {
  const {token} = useToken();
  const navigate = useNavigate();
  console.log(token);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  return (
    <div>
      <h1>Medical Data</h1>
    </div>
  );
}

export default MedicalData;
