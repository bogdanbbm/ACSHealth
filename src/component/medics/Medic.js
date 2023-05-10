import React, {useState} from "react";
import MedicReview from "./MedicReview";
import PropTypes from "prop-types";
import Modal from "@material-ui/core/Modal";

function Medic({medic}) {
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true);
    }

    const handleClose = () => {
        setOpen(false);
    }

    return (
        <div>
            <h1 >Medic</h1>
            <div className="medic-container" >
                <div className="medic-header">
                    <p onClick={handleOpen}>{medic.firstName} {medic.lastName}</p>
                    <p>{medic.rating}</p>
                </div>
                <div className="medic-reviews">
                    <Modal className="medic-modal" onClose={handleClose} open={open}>
                        <div className="medic-header">
                            <p>{medic.firstName} {medic.lastName}</p>
                            <p>{medic.rating}</p>
                            {medic.reviews.map(item => <MedicReview review={item} />)}
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