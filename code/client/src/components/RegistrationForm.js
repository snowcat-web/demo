import React from "react";
import SingupComplete from "./SingupComplete";

//Registration Form Component, process user info for online session.
//const textSingup = ;
const RegistrationForm = ({ selected, details }) => {
  if (selected !== -1) {
    return (
      <div className={`lesson-form`}>
        <div className={`lesson-desc`}>
          <h3>Registration details</h3>
          <div id="summary-table" className="lesson-info">
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
                />
              </div>
              <div className="lesson-input-box middle">
                <input
                  type="text"
                  id="email"
                  placeholder="Email"
                  autoComplete="cardholder"
                />
              </div>
              <div className="lesson-input-box last">
                <div className="lesson-card-element"></div>
              </div>
            </div>
            <div className="sr-field-error" id="card-errors" role="alert"></div>
            <div
              className="sr-field-error"
              id="customer-exists-error"
              role="alert"
              hidden
            >
              A customer with the email address of{" "}
              <span id="error_msg_customer_email"></span> already exists. If
              you'd like to update the card on file, please visit
              <span id="account_link"></span>.
            </div>
          </div>
          <button id="submit">
            <div className="spinner hidden" id="spinner"></div>
            <span id="button-text">Request Lesson</span>
          </button>
          <div className="lesson-legal-info">
            Your card will not be charged. By registering, you hold a session
            slot which we will confirm within 24 hrs.
          </div>
        </div>

        <SingupComplete active={false} email="" last4="" customer_id="" />
      </div>
    );
  } else {
    return "";
  }
};
export default RegistrationForm;
