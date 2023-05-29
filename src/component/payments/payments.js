import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';

async function checkIfMedic(token) {
    const apiURL = process.env.REACT_APP_API_URL;
    console.log(apiURL);
  
    return axios.get(apiURL + '/is_medic', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => response)
      .catch(error => console.log(error));
  }

function Payments({token}) {
    const navigate = useNavigate();
    console.log(token);
    useEffect(() => {
        if (!token) {
            navigate('/login');
        }
    }, [navigate, token]);
    const [isMedic, setIsMedic] = useState(true);

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

}

export default Payments;