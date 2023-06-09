// noinspection HtmlUnknownAttribute

import React, {useState} from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

async function submitReview(review, token, medicUsername) {
  const apiURL = process.env.REACT_APP_API_URL;
  return axios.post(apiURL + `/medic_reviews/${medicUsername}`, review, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => response)
    .catch(error => error.response);
}

function AddReview({token, medicUsername, closeModal, setReviews}) {
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();

    const response = await submitReview({
      rating,
      review: reviewText
    }, token, medicUsername);

    if (!response) {
      console.log('Unable to connect to the server.');
      return;
    }

    if (response.status === 201) {
      closeModal();
      setReviews(prevState => [...prevState, {rating, review: reviewText}]);
    } else {
      console.log(response);
    }
  }

  return (
    <div className="add-review-container">
      <form onSubmit={handleSubmit}>
        <div className="field">
          <input type="range" min="0" max="5" step="0.5" required className="slider" id="ratingSlider"
                 onChange={e => setRating(e.target.valueAsNumber)}/>
          <label for="ratingSlider">Rating: {rating}&#9733;</label>
        </div>
        <div className="field">
          <textarea className="review-text" rows="5" required id="reviewText"
                    onChange={e => setReviewText(e.target.value)}/>
          <label for="reviewText">Write your review here:</label>
        </div>
        <div className="field">
          <button type="submit">Add Review</button>
        </div>
      </form>
    </div>
  );
}

AddReview.propTypes = {
  token: PropTypes.string.isRequired,
  medicUsername: PropTypes.string.isRequired,
  closeModal: PropTypes.func.isRequired,
  setReviews: PropTypes.func.isRequired
}

export default AddReview;
