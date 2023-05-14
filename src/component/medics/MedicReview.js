import React from 'react';
import PropTypes from 'prop-types';

function MedicReview({ review }) {
    console.log(review);
    return (
        <div className="review-container">
            <h1>Medic Review</h1>
            <div className="review-body">
                <p>{review.rating}</p>
                <p>{review.review}</p>
            </div>
        </div>
    );
}

MedicReview.propTypes = {
    review : PropTypes.shape({
        rating: PropTypes.number.isRequired,
        review: PropTypes.string.isRequired
    }).isRequired
};

export default MedicReview;
