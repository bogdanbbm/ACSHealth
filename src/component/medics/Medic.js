import React from "react";
import MedicReview from "./MedicReview";
import PropTypes from "prop-types";

function Medic({medic}) {
    return (
        <div>
            <h1>Medic</h1>
            <div className="medic-container">
                <div className="medic-header">
                    <p>{medic.firstName} {medic.lastName}</p>
                    <p>{medic.rating}</p>
                </div>
                <div className="medic-reviews">
                    {medic.reviews.map(item => <MedicReview review={item} />)}
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