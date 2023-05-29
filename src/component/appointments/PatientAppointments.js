import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Appointments.css';
import Modal from '@material-ui/core/Modal';
import AddAppointment from './AddAppointment';

async function getPatientAppointments(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/appointments', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function Appointment({appointment}) {

  return (
    <div className="appointment">
      <h3>{appointment.appointmentDate}</h3>
      <h4>{appointment.medicUsername}</h4>
      <p>{appointment.clinicName}</p>
    </div>
  );
}

Appointment.propTypes = {
  appointment: PropTypes.shape({
    appointmentDate: PropTypes.string.isRequired,
    medicUsername: PropTypes.string.isRequired,
    clinicName: PropTypes.string.isRequired
  })
}

function PatientAppointments({token}) {
  const [appointments, setAppointments] = useState([]);

  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleOpen = () => {
    setOpen(true);
  }

  useEffect(() => {
    getPatientAppointments(token)
      .then(response => {
        if (response.status === 200) {
          setAppointments(response.data);
        } else {
          console.log(response);
        }
      });
  }, [token]);

  return (
    <>
      <div className="appointments">
        {appointments.map(appointment => (
          <Appointment appointment={appointment}/>))}
      </div>
      <div className="add-appointment">
        <button onClick={handleOpen}>Add appointment</button>
        <Modal className="add-appointment-modal" open={open} onClose={handleClose}>
          <div className="add-appointment-modal-container">
            <AddAppointment token={token} closeModal={handleClose} setAppointments={setAppointments}/>
          </div>
        </Modal>
      </div>
    </>
  );
}

PatientAppointments.propTypes = {
  token: PropTypes.string.isRequired
}

export default PatientAppointments;
