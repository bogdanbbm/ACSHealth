import React from 'react';
import useToken from "../../useToken";
import Login from "../login/Login";

function MedicalData() {
  const {token, setToken} = useToken();

  if (!token) {
    return <Login setToken={setToken} />
  }

  return (
    <div>
      <h1>Medical Data</h1>
    </div>
  );
}

export default MedicalData;
