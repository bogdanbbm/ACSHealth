import React from 'react';
import axios from 'axios';
import Medic from './Medic';
import './Medics.css';
import PropTypes from "prop-types";

async function getMedics() {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/medic_list', {
    headers: {
        'Content-Type': 'application/json'
    }
  })
    .then(response => response.data)
    .catch(error => console.log(error));
}

function getReviews(medicId) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/reviews/' + medicId, {
    headers: {
        'Content-Type': 'application/json'
    }
  })
    .then(response => response.data)
    .catch(error => console.log(error));
}

function Medics({ token }) {
  let medics = [{
    firstName: 'John',
    lastName: 'Doe',
    rating: 3.0,
    username: 'johndoe',
    reviews: [
      {
        rating: 4.5,
        review: 'Very good medic'
      },
      {
        rating: 1.5,
        review: 'Very bad medic'
      }
    ]
  },
    {
      firstName: 'Jane',
      lastName: 'Doe',
      rating: 4.0,
      username: 'janedoe',
      reviews: [
        {
          rating: 4.5,
          review: 'Very good medic'
        },
        {
          rating: 1.5,
          review: 'Very bad medic'
        }
      ]
    }
  ];
  // console.log(getMedics());

  if (!medics) {
    for (let i = 0; i < medics.length; i++) {
      medics[i].reviews = getReviews(medics[i].username);
    }
  }

  medics.sort((a, b) => (a.rating > b.rating) ? 1 : -1);

  return (
    <div className="medics">
        <h1>Medics</h1>
        <div className="medics-container">
            {medics.map(item => <Medic medic={item} token={token} />)}
        </div>
    </div>
  );
}

Medics.propTypes = {
  token: PropTypes.string.isRequired
}

export default Medics;
