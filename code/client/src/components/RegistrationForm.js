import React, {useCallback, useEffect, useState} from "react";
import { loadStripe } from "@stripe/stripe-js";
import {Elements} from "@stripe/react-stripe-js";
import SignupComplete from "./SignupComplete";
import CardElementForm from "./CardElementForm";
import {signupLesson} from "../Services/lessons";
import isEmail from "validator/lib/isEmail";

const promise = loadStripe("pk_test_51HIHnEI5c5rLhZzj8LtgFxt04cEQNDwhYTiz5uw8fvyv0o4PSrbr6cI5afXb9PgKGrxfG03G5y1k25eeeKl42zjA00t3kKsI9A");
const CUSTOMER_VALID_ERROR = "CUSTOMER_VALID_ERROR";

//Registration Form Component, process user info for online session.
//const textSignup = ;
export default function RegistrationForm({ selected, details, dateTime }) {
  const [disabled, setDisabled] = useState(true);
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [customExistError, setCustomExistError] = useState(null);
  const [signupComplete, setSignupComplete] = useState(false);
  const [customerInfo, setCustomerInfo] = useState({
    email: "",
    cus_id: ""
  })
  const [state, setStateValue] = useState({
    name: "",
    email: "",
    date_time: "",
    token: null
  })

  const handleChange = (e) => {
    setStateValue(state => ({
      ...state,
      [e.target.name]: e.target.value
    }))
    e.persist();
  }

  const handleCardChange = useCallback((cardDisabled, error, token=null) => {
    setDisabled(cardDisabled);
    setError(error);
    if (token) {
      setStateValue(state => ({
        ...state,
        token: JSON.parse(token)
      }))
    }
  }, []);

  const handleSubmit = async event => {
    event.preventDefault();
    if (!isEmail(state.email)) {
      setError("Please input valid email address");
    } else {
      setProcessing(true);
      setError("");

      let _response = await signupLesson(state);
      if (_response.error) {
        if (_response.error.code === CUSTOMER_VALID_ERROR) {
          setCustomExistError(true);
          setCustomerInfo({
            email: _response.error.email,
            cus_id: _response.error.cus_id
          })
        } else {
          setError(_response.error.message);
        }
        setProcessing(false);
      }

      if (_response.customer) {
        setCustomerInfo({
          email: _response.customer.email,
          cus_id: _response.customer.cus_id
        });
        setSignupComplete(true);
      }
    }
  }

  useEffect(() => {
    if (dateTime) {
      setStateValue(state => ({
        ...state,
        date_time: dateTime
      }))
    }
  }, [dateTime])

  if (selected !== -1) {
    return (
      <div className={`lesson-form`}>
        { !signupComplete && (
          <div className={`lesson-desc`}>
            <form
              id="lesson-signup-form"
              onSubmit={handleSubmit}
            >
              <h3>Registration details</h3>
              <div
                id="summary-tElable"
                className="lesson-info"
              >
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
                {error && (
                  <div
                    className="sr-field-error"
                    id="card-errors"
                    role="alert"
                  >
                    {error}
                  </div>
                )}
                { customExistError && (
                  <div
                    className="sr-field-error"
                    id="customer-exists-error"
                    role="alert"
                  >
                    A customer with the email address of
                    <span id="error_msg_customer_email"> {customerInfo.email} </span>
                    already exists. If
                    you'd like to update the card on file, please visit
                    <a
                      href={`/account_update/${customerInfo.cus_id}`}
                      id="account_link"
                    >
                      &nbsp;localhost:4242/account_update/{customerInfo.cus_id}
                    </a>.
                  </div>
                )}
              </div>
              { !customExistError && (
                <button
                  id="submit"
                  disabled={disabled || processing || !state.token}
                >
                  <div className="spinner hidden" id="spinner"></div>
                  <span id="button-text">Request Lesson</span>
                </button>
              )}
              <div className="lesson-legal-info">
                Your card will not be charged. By registering, you hold a session
                slot which we will confirm within 24 hrs.
              </div>
            </form>
          </div>
        )}
        <SignupComplete
          active={signupComplete}
          email={customerInfo.email}
          customer_id={customerInfo.cus_id}
          last4={state.token ? state.token.card.last4 : ""}
        />
      </div>
    );
  } else {
    return "";
  }
};
