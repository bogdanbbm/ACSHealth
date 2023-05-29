import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import Modal from '@material-ui/core/Modal';
import AddConsultation from './AddConsultation';
import './MedicalData.css';

async function getMedicConsultations(token) {
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
      <h4>{consultation.patientName}</h4>
      <p>{consultation.treatment}</p>
    </div>
  );
}

Consultation.propTypes = {
  consultation: PropTypes.shape({
    consultationDate: PropTypes.string.isRequired,
    patientName: PropTypes.string.isRequired,
    treatment: PropTypes.string.isRequired
  })
}

function MedicConsultations({ token }) {
  const [consultations, setConsultations] = useState([]);
  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleOpen = () => {
    setOpen(true);
  }

  useEffect(() => {
    getMedicConsultations(token)
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
      <h1 className="consultations-h1">MConsultations</h1>
      <div className="consultations">
        {consultations.map(consultation => (
          <Consultation consultation={consultation} />))}
      </div>
      <div className="add-consultation">
        <button onClick={handleOpen}>Add consultation</button>
        <Modal className="add-consultation-modal" open={open} onClose={handleClose}>
          <div className="add-consultation-modal-container">
            <AddConsultation token={token} setConsultations={setConsultations} closeModal={handleClose}/>
          </div>
        </Modal>
      </div>
    </>
  );
}

MedicConsultations.propTypes = {
  token: PropTypes.string.isRequired
}

export default MedicConsultations;
