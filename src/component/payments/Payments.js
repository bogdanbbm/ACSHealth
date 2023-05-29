import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';
import MedicPayments from './MedicPayment';
import Modal from '@material-ui/core/Modal';
import AddPayment from './AddPayment';
import './Payments.css';
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

function Payments({token}) {
  const navigate = useNavigate();
  console.log(token);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [navigate, token]);

  const [payments, setPayments] = useState([]);

  const [isMedic, setIsMedic] = useState(false);

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

  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleOpen = () => {
    setOpen(true);
  }


  return (
      <div className="payments-overview">
        <div className="bg"/>
        <h1>Your Payments</h1>
          <div className="payments-container">
            <MedicPayments token={token}/>
          </div>
          <div className="add-payment">
          <button onClick={handleOpen}>Add payment</button>
          <Modal className="add-payment-modal" open={open} onClose={handleClose}>
            <div className="add-payment-modal-container">
              <AddPayment token={token} closeModal={handleClose} setPayments={setPayments}/>
            </div>
          </Modal>
        </div>
      </div>
  );
}

Payments.propTypes = {
  token: PropTypes.string.isRequired
};

export default Payments;
