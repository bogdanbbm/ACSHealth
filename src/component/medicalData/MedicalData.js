import React from 'react';
import useToken from "../../hooks/useToken";
import Login from "../login/Login";

function MedicalData() {
  // const {token, setToken} = useToken();
  //
  // if (!token) {
  //   return <Login setToken={setToken} />
  // }

    var personal_data = [];
    var medical_history = [];


  return (
    <div className="login-wrapper">
      <h1>Medical Data</h1>
        <div>
            <h2>Personal Data</h2>
            <ul id="personal_data_list"></ul>
            <h2>Medical History</h2>
            <ul id="medical_history_list"></ul>
        </div>

    </div>
  );
}

export default MedicalData;
