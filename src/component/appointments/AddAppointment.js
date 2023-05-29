import React, {useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Appointments.css';

async function submitAppointment(token, appointment) {
    const apiURL = process.env.REACT_APP_API_URL;

    return axios.post(apiURL + '/appointments', appointment, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response)
        .catch(error => console.log(error));
}

function AddAppointment({ token, closeModal, setAppointments }) {
    const [appointment, setAppointment] = useState({
        medicUsername: '',
        appointmentDate: '',
        clinicName: ''
    });

    const onInputChange = e => {
        setAppointment({
            ...appointment,
            [e.target.name]: e.target.value
        });
    }

    const handeSubmit = e => {
        e.preventDefault();
        submitAppointment(token, appointment)
            .then(response => {
                if (response.status === 201) {
                    closeModal();
                    setAppointments(prevState => [...prevState, appointment]);
                } else {
                    console.log(response);
                }
                }
            );
    }

    return (
        <div className="add-appointment-container">
            <form onSubmit={handeSubmit}>
                <div className="field">
                    <label htmlFor="medicusername">Medic Username</label>
                    <input type="text" id="medicusername" name="medicUsername" required onChange={onInputChange}/>
                </div>
                <div className="field">
                    <label htmlFor="appointmentDate">Appointment Date</label>
                    <input type="date" id="appointmentDate" name="appointmentDate" required onChange={onInputChange}/>
                </div>
                <div className="field">
                    <label htmlFor="clinicName">Clinic Name</label>
                    <textarea className="clinicName-text" rows="5" id="clinicName" name="clinicName" required onChange={onInputChange}/>
                </div>
                <div className="field">
                    <button type="submit">Add Appointment</button>
                </div>
            </form>
        </div>
    );
}

AddAppointment.propTypes = {
    token: PropTypes.string.isRequired,
    closeModal: PropTypes.func.isRequired,
    setAppointments: PropTypes.func.isRequired
}

export default AddAppointment;
