import React, {useEffect, useState} from 'react';
import MedicReview from './MedicReview';
import PropTypes from 'prop-types';
import Modal from '@material-ui/core/Modal';
import './Medics.css';
import AddReview from './AddReview';
import axios from "axios";

function getReviews(medicId) {
  const apiURL = process.env.REACT_APP_API_URL;

  return axios.get(apiURL + '/reviews/' + medicId, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response)
    .catch(error => console.log(error));
}

function Medic({ medic, token }) {
  const [open, setOpen] = useState(false);
  const [openAddReview, setOpenAddReview] = useState(false);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    getReviews(medic.id)
      .then(response => {
        if (response.status === 200) {
          setReviews(response.data);
        } else {
          console.log(response);
        }
      });
  }, [medic.id]);

  const handleOpen = () => {
    setOpen(true);
  }

  const handleOpenAddReview = () => {
    setOpenAddReview(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  const handleCloseAddReview = () => {
    setOpenAddReview(false);
  }

  return (
    <div className="medic-container" >
      <div className="medic-header">
        <h1>{medic.firstName} {medic.lastName}</h1>
        <img src="https://via.placeholder.com/150" alt="Medic" />
      </div>
      <div className="medic-body">
        <div className="medic-details">
          <h3>Primary Medic</h3>
          <p>
            Rating: {medic.rating.toFixed(2)}<br/>
            Number of reviews: {reviews.length}
          </p>
        </div>
        <div className="medic-reviews">
          <button onClick={handleOpen}>View reviews</button>
          <Modal className="medic-modal" onClose={handleClose} open={open}>
            <div className="modal-container">
              <div className="medic-header">
                <h1>{medic.firstName} {medic.lastName}</h1>
                <img src="https://via.placeholder.com/150" alt="Medic" />
              </div>
              <div className="medic-body">
                <div className="medic-details">
                  <h3>Primary Medic</h3>
                  <p>
                    Rating: {medic.rating.toFixed(2)}<br/>
                    Number of reviews: {reviews.length}
                  </p>
                </div>
                <div className="medic-reviews">
                  {reviews.map(item => <MedicReview review={item} />)}
                </div>
                <div className="add-review-button">
                  {token && <button onClick={handleOpenAddReview}>Add review</button>}
                  <Modal className="add-review-modal" onClose={handleCloseAddReview} open={openAddReview}>
                    <div className="add-review-modal-container">
                      <AddReview token={token} medicUsername={medic.username} closeModal={handleCloseAddReview}/>
                    </div>
                  </Modal>
                </div>
              </div>
            </div>
          </Modal>
        </div>
      </div>
    </div>
  );
}

Medic.propTypes = {
  medic: PropTypes.shape({
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    rating: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
  }).isRequired,
  token: PropTypes.string.isRequired
}

export default Medic;
