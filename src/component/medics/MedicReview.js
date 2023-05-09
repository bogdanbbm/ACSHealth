import React from "react";
import PropTypes from "prop-types";
//     review(username) = review(text), rating(float)
function MedicReview({review}) {
    console.log(review);
    return (
        <div>
            <h1>Medic Review</h1>
            <div className="review-container">
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