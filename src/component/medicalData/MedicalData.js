import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';
import PatientConsultations from './PatientConsultations';
import MedicConsultations from './MedicConsultations';
import './MedicalData.css';

async function checkIfCompleted(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/has_completed', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

async function getPersonalData(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/patient_data', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

async function updatePersonalData(token, personalData) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.put(apiURL + '/patient_data', personalData, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

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

function MedicalData({token}) {
  const navigate = useNavigate();
  console.log(token);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  const [isMedic, setIsMedic] = useState(true);
  const [hasCompleted, setHasCompleted] = useState(true);
  const [personalData, setPersonalData] = useState({
    firstName: '',
    lastName: '',
    cnp: '',
    birthDate: '',
    sex: '',
    height: 0.0,
    weight: 0.0,
    bloodGroup: '',
    rh: '',
    allergies: '',
  });
  const [editMode, setEditMode] = useState(false);
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

  useEffect(() => {
    checkIfCompleted(token)
      .then(response => {
        if (response.status === 200) {
          setHasCompleted(response.data.completed);
        } else {
          console.log(response.data);
        }
      });
  }, [token]);

  useEffect(() => {
    if (hasCompleted) {
      getPersonalData(token)
        .then(response => {
          if (response.status === 200) {
            setPersonalData(response.data);
            setEditMode(false);
          } else {
            console.log(response.data);
          }
        });
    } else {
      setEditMode(true);
    }
  }, [hasCompleted, token]);

  const onInputChange = e => {
    setPersonalData({
      ...personalData,
      [e.target.name]: e.target.value
    });
  }

  const handleSubmit = e => {
    e.preventDefault();
    updatePersonalData(token, personalData)
      .then(response => {
        if (response.status === 200) {
          setEditMode(false);
          setError('');
        } else {
          setError(response.data.message);
        }
      }
    );
  }

  return (
    <div className="data">
      <div className={"bg"}/>
      <h1>Personal Data</h1>
      <div className="personal-data-container">
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label for="firstname">First Name:</label>
            {editMode ? <input type="text" name="firstName" id="firstname" onChange={onInputChange}/> :
              <span>{personalData?.firstName}</span>}
          </div>
          <div className="field">
            <label for="lastname">Last Name:</label>
            {editMode ? <input type="text" name="lastName" id="lastname" onChange={onInputChange}/> :
              <span>{personalData?.lastName}</span>}
          </div>
          <div className="field">
            <label for="cnp">CNP:</label>
            {editMode ? <input type="text" name="cnp" id="cnp" onChange={onInputChange}/> : <span>{personalData?.cnp}</span>}
          </div>
          <div className="field">
            <label for="birthdate">Birthday:</label>
            {editMode ? <input type="date" name="birthDate" id="birthdate" onChange={onInputChange}/> :
              <span>{personalData?.birthDate}</span>}
          </div>
          <div className="field">
            <label for="sex">Sex:</label>
            {editMode ? <select name="sex" id="sex" onChange={onInputChange}>
              <option hidden selected>Choose sex</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select> : <span>{personalData?.sex}</span>}
          </div>
          <div className="field">
            <label for="height">Height (cm):</label>
            {editMode ? <input type="number" min="0" name="height" id="height" onChange={onInputChange}/> :
              <span>{personalData?.height}</span>}
          </div>
          <div className="field">
            <label for="weight">Weight (kg):</label>
            {editMode ? <input type="number" min="0" name="weight" id="weight" onChange={onInputChange}/> :
              <span>{personalData?.weight}</span>}
          </div>
          <div className="field">
            <label for="bloodgroup">Blood Group:</label>
            {editMode ? <select name="bloodGroup" id="bloodgroup" onChange={onInputChange}>
              <option hidden selected>Choose blood group</option>
              <option value="01">01</option>
              <option value="A2">A2</option>
              <option value="B3">B3</option>
              <option value="AB4">AB4</option>
            </select> : <span>{personalData?.bloodGroup}</span>}
          </div>
          <div className="field">
            <label for="rh">Rh:</label>
            {editMode ? <select name="rh" id="rh" onChange={onInputChange}>
              <option hidden selected>Choose Rh</option>
              <option value="+">+</option>
              <option value="-">-</option>
            </select> : <span>{personalData?.rh}</span>}
          </div>
          <div className="field">
            <label for="allergies">Allergies:</label>
            {editMode ? <input type="text" name="allergies" id="allergies" onChange={onInputChange}/> :
              <span>{personalData?.allergies}</span>}
          </div>
          <div className="save-edit-button">
            {editMode && <button type="submit">Save</button>}
            {!editMode && <button onClick={() => setEditMode(true)}>Edit</button>}
            {error && <span className="err">{error}</span>}
          </div>
        </form>
      </div>
      <div className="consultations-container">
        {isMedic ? <MedicConsultations token={token}/> : <PatientConsultations token={token}/> }
      </div>
    </div>
  );
}

MedicalData.propTypes = {
  token: PropTypes.string.isRequired
};

export default MedicalData;
