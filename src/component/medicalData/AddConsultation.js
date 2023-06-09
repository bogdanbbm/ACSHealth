import React, {useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './MedicalData.css';

async function submitConsultation(token, consultation) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.post(apiURL + '/medical_data', consultation, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function AddConsultation({ token, closeModal, setConsultations }) {
  const [consultation, setConsultation] = useState({
    patientUsername: '',
    consultationDate: '',
    treatment: ''
  });

  const onInputChange = e => {
    setConsultation({
      ...consultation,
      [e.target.name]: e.target.value
    });
  }

  const handeSubmit = e => {
    e.preventDefault();
    submitConsultation(token, consultation)
      .then(response => {
        if (response.status === 201) {
          closeModal();
          setConsultations(prevState => [...prevState, consultation])
        } else {
          console.log(response);
        }
      }
    );
  }

  return (
    <div className="add-consultation-container">
      <form onSubmit={handeSubmit}>
        <div className="field">
          <label htmlFor="patientusername">Patient Username</label>
          <input type="text" id="patientusername" name="patientUsername" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <label htmlFor="consultationDate">Date</label>
          <input type="date" id="consultationDate" name="consultationDate" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <label htmlFor="treatment">Treatment</label>
          <textarea className="treatment-text" rows="5" id="treatment" name="treatment" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <button type="submit">Add consultation</button>
        </div>
      </form>
    </div>
  );
}

AddConsultation.propTypes = {
  token: PropTypes.string.isRequired,
  closeModal: PropTypes.func.isRequired,
  setConsultations: PropTypes.func.isRequired
}

export default AddConsultation;
