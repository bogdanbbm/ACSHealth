import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Appointments.css';

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

function Appointment({ appointment }) {

    return (
        <div>
            <h3>{appointment.appointmentDate}</h3>
            <h4>{appointment.medicUsername}</h4>
            <p>{appointment.clinicName}</p>
        </div>
    );
}

Appointment.propTypes = {
    consultation: PropTypes.shape({
        appointmentDate: PropTypes.string.isRequired,
        medicUsername: PropTypes.string.isRequired,
        clinicName: PropTypes.string.isRequired
    })
}

function PatientAppointmens({ token }) {
    const [appointments, setAppointments] = useState([]);

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
        <div className="appointments">
            <h1>PAppointments</h1>
            {appointments.map(appointment => (
                <Appointment appointment={appointment} />))}
        </div>
    );
}

PatientAppointmens.propTypes = {
    token: PropTypes.string.isRequired
}

export default PatientAppointmens;
