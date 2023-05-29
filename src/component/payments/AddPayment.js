import React, {useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Payments.css';

async function submitPayment(token, payment) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.post(apiURL + '/payments', payment, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function AddPayment({token, closeModal, setPayments}) {
  const [payment, setPayment] = useState({
    firstName: '',
    lastName: '',
    value: 0.0,
    paymentDate: '',
    patientUsername: '',
    currency: ''
  });

  const onInputChange = e => {
    setPayment({
      ...payment,
      [e.target.name]: e.target.value
    });
  }

  const handeSubmit = e => {
    e.preventDefault();
    submitPayment(token, payment)
      .then(response => {
          if (response.status === 201) {
            closeModal();
            setPayments(prevState => [...prevState, payment]);
          } else {
            console.log(response);
          }
        }
      );
  }

  return (
    <div className="add-payment-container">
      <form onSubmit={handeSubmit}>
        <div className="field">
          <label htmlFor="patientUsername">Patient Username</label>
          <input type="text" id="patientUsername" name="patientUsername" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <label htmlFor="paymentDate">Payment Date</label>
          <input type="date" id="paymentDate" name="paymentDate" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <label htmlFor="currency">Currency Name</label>
          <input className="currency-text" id="currency" name="currency" required
                    onChange={onInputChange}/>
        </div>
        <div className="field">
          <label htmlFor="value">Value</label>
          <input type="text" id="value" name="value" required onChange={onInputChange}/>
        </div>
        <div className="field">
          <button type="submit">Add payment</button>
        </div>
      </form>
    </div>
  );
}

AddPayment.propTypes = {
  token: PropTypes.string.isRequired,
  closeModal: PropTypes.func.isRequired,
  setpayments: PropTypes.func.isRequired
}

export default AddPayment;
