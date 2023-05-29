import React, {useEffect, useState} from 'react';
import axios from 'axios';
import Medic from './Medic';
import './Medics.css';
import PropTypes from 'prop-types';

async function getMedics() {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/medic_list', {
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function Medics({token}) {
  const [medics, setMedics] = useState([]);

  useEffect(() => {
    getMedics()
      .then(response => {
        if (response.status === 200) {
          setMedics(response.data);
        } else {
          console.log(response);
        }
      });
  }, []);

  useEffect(() => {
    medics.sort((a, b) => (a.rating > b.rating) ? 1 : -1);
  }, [medics]);

  return (
    <div className="medics">
      <h1>Medics</h1>
      <div className="medics-container">
        {medics.map(item => <Medic medic={item} token={token}/>)}
      </div>
    </div>
  );
}

Medics.propTypes = {
  token: PropTypes.string.isRequired
}

export default Medics;
