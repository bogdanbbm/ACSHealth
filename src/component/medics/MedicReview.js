import React from 'react';
import PropTypes from 'prop-types';

function MedicReview({ review }) {
    console.log(review);
    return (
        <div className="review-container">
            <div className="review-body">
                <h4>Rating: {review.rating}</h4>
                <p style={{textAlign: "left"}}>{review.review}</p>
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
