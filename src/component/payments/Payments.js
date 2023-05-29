import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';
import PatientPayments from './PatientPayments';
import MedicPayments from './MedicPayments';
import './Payments.css';
async function checkIfMedic(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/is_medic', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));

function Payments({token}) {
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  const [isMedic, setIsMedic] = useState(false);

  useEffect(() => {
    checkIfMedic(token)
      .then(response => {
        if (response.status === 200) {
          setIsMedic(response.data.isMedic);
        } else {
          console.log(response.data);
        }
      });
  }, [token]);

  return (
    <div className="payments-overview">
      <div className="bg"/>
      <h1>Your Payments</h1>
      <div className="payments-container">
        {isMedic ? <MedicPayments token={token}/> : <PatientPayments token={token}/> }
      </div>
    </div>
  );
}

Payments.propTypes = {
  token: PropTypes.string.isRequired
};

export default Payments;
