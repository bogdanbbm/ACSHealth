import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';
import PatientAppointments from './PatientAppointments';
import MedicAppointments from './MedicAppointments';
import './Appointments.css';
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
}

function Appointments({token}) {
  const navigate = useNavigate();
  console.log(token);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  const [isMedic, setIsMedic] = useState(false);
  const [error, setError] = useState('');

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
      <div className="appointments-overview">
        <div className="bg"/>
        <h1>Your Appointments</h1>
        <div className="appointments-container">
          {isMedic ? <MedicAppointments token={token}/> : <PatientAppointments token={token}/> }
        </div>
      </div>
  );
}

Appointments.propTypes = {
  token: PropTypes.string.isRequired
};

export default Appointments;
