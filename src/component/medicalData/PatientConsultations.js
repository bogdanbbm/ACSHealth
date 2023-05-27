import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

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
    <div>
      <h3>{consultation.date}</h3>
      <h4>{consultation.medicName}</h4>
      <p>{consultation.treatment}</p>
    </div>
  );
}

Consultation.propTypes = {
  consultation: PropTypes.shape({
    date: PropTypes.string.isRequired,
    medicName: PropTypes.string.isRequired,
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
    <div className="consultations">
      <h1>PConsultations</h1>
      {consultations.map(consultation => (
        <Consultation consultation={consultation} />))}
    </div>
  );
}

PatientConsultations.propTypes = {
  token: PropTypes.string.isRequired
}

export default PatientConsultations;
