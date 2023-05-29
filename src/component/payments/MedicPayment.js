import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Payments';

async function getMedicPayment(token) {
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

function Payment({payment}) {

  return (
    <div className='payment'>
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
  appointment: PropTypes.shape({
    appointmentDate: PropTypes.string.isRequired,
    patientUsername: PropTypes.string.isRequired,
    clinicName: PropTypes.string.isRequired
  })
}

function MedicPayments({token}) {
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    getMedicPayment(token)
      .then(response => {
        if (response.status === 200) {
          setPayments(response.data);
        } else {
          console.log(response);
        }
      });
  }, [token]);

  return (
    <div className="payments">
      {payments.map(payment => (
        <Payment payment={payment}/>))}
    </div>
  );
}

MedicPayments.propTypes = {
  token: PropTypes.string.isRequired
}

export default MedicPayments;
