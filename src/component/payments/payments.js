import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import PropTypes from 'prop-types';
import axios from 'axios';


// payments

function Payment({ payment }) {

  return (
    <div>
      <h3>{payment.firstName}</h3>
      <h4>{payment.lastName}</h4>
      <p>{payment.value}</p>
      <p>{payment.paymentDate}</p>
      <p>{payment.patientUsername}</p>
      <p>{payment.currency}</p>

    </div>
  );
}

Payment.propTypes = {
  payment: PropTypes.shape({
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    value: PropTypes.number.isRequired,
    paymentDate: PropTypes.string.isRequired,
    patientUsername: PropTypes.string.isRequired,
    currency: PropTypes.string.isRequired
  })
}


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

async function getPayments(token) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/payments', {
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

    const [payments, setPayments] = useState([]);
    const [isMedic, setIsMedic] = useState(true);
    const [hasCompleted, setHasCompleted] = useState(true);

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
      getPayments(token)
        .then(response => {
          if (response.status === 200) {
            setPayments(response.data);
          } else {
            console.log(response.data);
          }
        });
  }, [token]);
  console.log(payments);

  if(isMedic)
    return (
      // <div className="consultations-container">
      //     {isMedic ? <MedicConsultations token={token}/> : <PatientConsultations token={token}/> }
      // </div>
      <div className="payments">
          <h1>Payments</h1>
          {payments.map(payment => (
            <Payment consultation={payment} />))}
      </div>
    );
  return(<p></p>);

}

export default Payments;