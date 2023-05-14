import React, { useState } from 'react';
import MedicReview from './MedicReview';
import PropTypes from 'prop-types';
import Modal from '@material-ui/core/Modal';
import './Medics.css';

function Medic({ medic }) {
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true);
    }

    const handleClose = () => {
        setOpen(false);
    }

    return (
        <div className="medic-container" >
            <div className="medic-header">
                <h1>{medic.firstName} {medic.lastName}</h1>
                <img src="https://via.placeholder.com/150" alt="Medic" />
            </div>
            <div className="medic-body">
                <div className="medic-details">
                    <p>Primary Medic</p>
                    <p>
                        Rating: {medic.rating.toFixed(2)}<br/>
                        Number of reviews: {medic.reviews.length}
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
                                    <p>Primary Medic</p>
                                    <p>
                                        Rating: {medic.rating.toFixed(2)}<br/>
                                        Number of reviews: {medic.reviews.length}
                                    </p>
                                </div>
                                <div className="medic-reviews">
                                    {medic.reviews.map(item => <MedicReview review={item} />)}
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
        reviews: PropTypes.arrayOf(PropTypes.object).isRequired
    }).isRequired
}

export default Medic;
