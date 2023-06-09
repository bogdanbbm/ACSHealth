import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './MedicalData.css';

async function getPatientConsultations(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/medical_data', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function Consultation({ consultation }) {

  return (
    <div className="consultation">
      <h3>{consultation.consultationDate}</h3>
      <h4>{consultation.medicUsername}</h4>
      <p>{consultation.treatment}</p>
    </div>
  );
}

Consultation.propTypes = {
  consultation: PropTypes.shape({
    consultationDate: PropTypes.string.isRequired,
    medicUsername: PropTypes.string.isRequired,
    treatment: PropTypes.string.isRequired
  })
}

function PatientConsultations({ token }) {
  const [consultations, setConsultations] = useState([]);

  useEffect(() => {
    getPatientConsultations(token)
      .then(response => {
        if (response.status === 200) {
          setConsultations(response.data);
        } else {
          console.log(response);
        }
      });
  }, [token]);

  return (
    <>
      <h1 className="consultations-h1">Consultations</h1>
      <div className="consultations">
        {consultations.map(consultation => (
          <Consultation consultation={consultation} />))}
      </div>
    </>
  );
}

PatientConsultations.propTypes = {
  token: PropTypes.string.isRequired
}

export default PatientConsultations;
