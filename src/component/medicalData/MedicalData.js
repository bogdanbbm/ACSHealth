import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';

async function checkIfCompleted(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/has_completed', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response.data)
    .catch(error => console.log(error));
}

async function getPersonalData(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/personal_data', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response.data)
    .catch(error => console.log(error));
}


function MedicalData({ token }) {
  const navigate = useNavigate();
  console.log(token);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);
  
  const [hasCompleted, setHasCompleted] = useState(false);
  const [personalData, setPersonalData] = useState();
  const [editMode, setEditMode] = useState(true);
  
  useEffect(() => {
    checkIfCompleted(token)
      .then(response => {
        setHasCompleted(response);
      });
  }, [token]);

  useEffect(() => {
    if (hasCompleted) {
      getPersonalData(token)
        .then(response => {
          setPersonalData(response);
          setEditMode(false);
        });
    }
  }, [hasCompleted, token]);

  return (
    <div>
      <h1>Personal Data</h1>
      <div>
        <form>
          <div>
            <label for="firstname">First Name:</label>
            {editMode ? <input name="firstname" id="firstname"></input> : <span>{personalData?.firstName}</span>}
          </div>
          <div>
            <label for="lastname">Last Name:</label>
            {editMode ? <input name="lastname" id="lastname"></input> : <span>{personalData?.lastName}</span>}
          </div>
          <div>
            <label for="cnp">CNP:</label>
            {editMode ? <input name="cnp" id="cnp"></input> : <span>{personalData?.cnp}</span>}
          </div>
          <div>
            <label for="birthdate">Birthday:</label>
            {editMode ? <input type="date" name="birthdate" id="birthdate"></input> : <span>{personalData?.birthDate}</span>}
          </div>
          <div>
            <label for="sex">Sex:</label>
            {editMode ? <select name="sex" id="sex">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select> : <span>{personalData?.sex}</span>}
          </div>
          <div>
            <label for="height">Height:</label>
            {editMode ? <input name="height" id="height"></input> : <span>{personalData?.height}</span>}
          </div>
          <div>
            <label for="weight">Weight:</label>
            {editMode ? <input name="weight" id="weight"></input> : <span>{personalData?.weight}</span>}
          </div>
          <div>
            <label for="bloodgroup">Blood Group:</label>
            {editMode ? <select name="bloodgroup" id="bloodgroup">
              <option value="01">01</option>
              <option value="A2">A2</option>
              <option value="B3">B3</option>
              <option value="AB4">AB4</option>
            </select> : <span>{personalData?.bloodGroup}</span>}
          </div>
          <div>
            <label for="rh">Rh:</label>
            {editMode ? <select name="rh" id="rh">
              <option value="+">+</option>
              <option value="-">-</option>
            </select> : <span>{personalData?.rh}</span>}
          </div>
          <div>
            <label for="allergies">Allergies:</label>
            {editMode ? <input name="allergies" id="allergies"></input> : <span>{personalData?.allergies}</span>}
          </div>
        </form>
      </div>
    </div>
  );
}

MedicalData.propTypes = { 
  token: PropTypes.string.isRequired
};

export default MedicalData;