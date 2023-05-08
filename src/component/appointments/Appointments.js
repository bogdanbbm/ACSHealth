import React, {useEffect} from 'react';
import useToken from "../../hooks/useToken";
import { useNavigate } from "react-router-dom";

function MedicalData() {
  const {token} = useToken();
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  return (
    <div>
      <h1>Appointments</h1>
    </div>
  );
}

export default MedicalData;
