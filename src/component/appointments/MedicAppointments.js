import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Appointments.css';

async function getMedicAppointments(token) {
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
      <h4>{appointment.patientUsername}</h4>
      <p>{appointment.clinicName}</p>
    </div>
  );
}

Appointment.propTypes = {
  appointment: PropTypes.shape({
    appointmentDate: PropTypes.string.isRequired,
    patientUsername: PropTypes.string.isRequired,
    clinicName: PropTypes.string.isRequired
  })
}

function MedicAppointments({token}) {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    getMedicAppointments(token)
      .then(response => {
        if (response.status === 200) {
          setAppointments(response.data);
        } else {
          console.log(response);
        }
      });
  }, [token]);

  return (
    <div className="appointments">
      {appointments.map(appointment => (
        <Appointment appointment={appointment}/>))}
    </div>
  );
}

MedicAppointments.propTypes = {
  token: PropTypes.string.isRequired
}

export default MedicAppointments;
