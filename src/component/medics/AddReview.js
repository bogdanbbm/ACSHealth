import React from 'react';
import PropTypes from 'prop-types';

function AddReview({ token })
{
    return (
        <div className="review-container">
            <p>Review</p>
        </div>
    );
}

AddReview.propTypes = {
    token : PropTypes.string.isRequired
}

export default AddReview;
