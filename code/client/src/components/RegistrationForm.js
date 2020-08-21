import React, {useState} from "react";
import { loadStripe } from "@stripe/stripe-js";
import {Elements} from "@stripe/react-stripe-js";
import SignupComplete from "./SingupComplete";
import CardElementForm from "./CardElementForm";
import {signupLesson} from "../Services/lessons";

const promise = loadStripe("pk_test_51HIHnEI5c5rLhZzj8LtgFxt04cEQNDwhYTiz5uw8fvyv0o4PSrbr6cI5afXb9PgKGrxfG03G5y1k25eeeKl42zjA00t3kKsI9A");

//Registration Form Component, process user info for online session.
//const textSignup = ;
export default function RegistrationForm({ selected, details }) {
  const [disabled, setDisabled] = useState(true);
  const [cardError, setCardError] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [customExistError, setCustomExistError] = useState(null);
  const [state, setStateValue] = useState({
    name: "",
    email: "",
    token: null
  })

  const handleChange = (e) => {
    setStateValue(state => ({
      ...state,
      [e.target.name]: e.target.value
    }))
  }

  const handleCardChange = (cardDisabled, error, token=null) => {
    setDisabled(cardDisabled);
    setCardError(error);
    if (token) {
      setStateValue(state => ({
        ...state,
        token: JSON.parse(token)
      }))
    }
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setProcessing(true);
    signupLesson(state)
      .then(response => console.log(response.data))
  }

  if (selected !== -1) {
    return (
      <div className={`lesson-form`}>
        <div className={`lesson-desc`}>
          <form id="lesson-signup-form" onSubmit={handleSubmit}>
            <h3>Registration details</h3>
            <div id="summary-tElable" className="lesson-info">
              {details}
            </div>
            <div className="lesson-grid">
              <div className="lesson-inputs">
                <div className="lesson-input-box first">
                  <input
                    type="text"
                    id="name"
                    placeholder="Name"
                    autoComplete="cardholder"
                    className="sr-input"
                    name="name"
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="lesson-input-box middle">
                  <input
                    type="text"
                    id="email"
                    placeholder="Email"
                    autoComplete="cardholder"
                    name="email"
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="lesson-input-box last">
                  <div className="lesson-card-element">
                    <Elements stripe={promise}>
                      <CardElementForm handleChange={handleCardChange}/>
                    </Elements>
                  </div>
                </div>
              </div>
              {cardError && (
                <div
                  className="sr-field-error"
                  id="card-errors"
                  role="alert"
                >
                  {cardError}
                </div>
              )}
              { customExistError && (
                <div
                  className="sr-field-error"
                  id="customer-exists-error"
                  role="alert"
                >
                  A customer with the email address of{" "}
                  <span id="error_msg_customer_email"></span> already exists. If
                  you'd like to update the card on file, please visit
                  <span id="account_link"></span>.
                </div>
              )}
            </div>
            <button
              id="submit"
              disabled={disabled || processing}
            >
              <div className="spinner hidden" id="spinner"></div>
              <span id="button-text">Request Lesson</span>
            </button>
            <div className="lesson-legal-info">
              Your card will not be charged. By registering, you hold a session
              slot which we will confirm within 24 hrs.
            </div>
          </form>
        </div>
        <SignupComplete
          active={false}
          email=""
          last4=""
          customer_id=""
        />
      </div>
    );
  } else {
    return "";
  }
};
