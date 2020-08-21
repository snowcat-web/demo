import React, {useEffect, useState} from "react";
import {CardElement, useElements, useStripe} from "@stripe/react-stripe-js";

export default function CardElementForm(props) {
  const [error, setError] = useState(null);
  const [disabled, setDisabled] = useState(true);
  const [token, setToken] = useState(null);
  const elements = useElements();
  const stripe = useStripe();

  const handleChange = async (event) => {
    // Listen for changes in the CardElement
    // and display any errors as the customer types their card details
    setDisabled(event.empty);
    setError(event.error ? event.error.message : "");
    stripe.createToken(elements.getElement(CardElement))
      .then(response => {
        if (response.error) {
          setError(response.error.message)
        } else {
          setToken(response.token);
        }
      })
  };

  useEffect(() => {
    props.handleChange(disabled, error, JSON.stringify(token));
  }, [disabled, error, token, props]);

  return (
    <CardElement
      id="card-element"
      onChange={handleChange}
    />
  );
}