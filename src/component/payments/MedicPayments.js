import React, {useEffect, useState} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Payments.css';
import Modal from '@material-ui/core/Modal';
import AddPayment from './AddPayment';

async function getMedicPayments(token) {
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
      <p>{payment.value}{payment.currency}</p>
      <p>{payment.paymentDate}</p>
      <p>{payment.patientUsername}</p>
    </div>
  );
}

Payment.propTypes = {
  payment: PropTypes.shape({
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    value: PropTypes.number.isRequired,
    currency: PropTypes.string.isRequired,
    paymentDate: PropTypes.string.isRequired,
    patientUsername: PropTypes.string.isRequired
  })
}

function MedicPayments({token}) {
  const [payments, setPayments] = useState([]);
  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleOpen = () => {
    setOpen(true);
  }

  useEffect(() => {
    getMedicPayments(token)
      .then(response => {
        if (response.status === 200) {
          setPayments(response.data);
        } else {
          console.log(response);
        }
      });
  }, [token]);

  return (
    <>
      <div className="payments">
        {payments.map(payment => (
          <Payment payment={payment}/>))}
      </div>
      <div className="add-payment">
        <button onClick={handleOpen}>Add payment</button>
        <Modal className="add-payment-modal" open={open} onClose={handleClose}>
          <div className="add-payment-modal-container">
            <AddPayment token={token} closeModal={handleClose} setPayments={setPayments}/>
          </div>
        </Modal>
      </div>
    </>
  );
}

MedicPayments.propTypes = {
  token: PropTypes.string.isRequired
}

export default MedicPayments;
