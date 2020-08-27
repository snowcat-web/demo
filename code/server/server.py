#! /usr/bin/env python3.6

"""
server.py
Stripe Card Payments Certification.
Python 3.6 or newer required.
"""

import json
import os
import time
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, find_dotenv

import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

load_dotenv(find_dotenv())

static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))

frontend = ""
if os.path.isfile("/".join([static_dir, "index.html"])):
    frontend = "vanilla"
else:
    frontend = "react"
    static_dir = str(os.path.abspath(os.path.join(__file__, "..", "./templates")))

server_dir = str(os.path.abspath(os.path.join(__file__, "../..")))

courseInfo = {}
with open(os.path.join(server_dir, "items.json")) as f:
    courseInfoJson = json.load(f)

for video in courseInfoJson:
    courseInfo[video["itemId"]] = video

with open(os.path.join(server_dir, "config.json")) as f:
    configInfo = json.load(f)

app = Flask(
    __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
)


### Get started! Shows the main page of the challenge with links to the
# different sections.
@app.route("/", methods=["GET"])
def get_main_page():
    # Display checkout page
    if frontend == "vanilla":
        return render_template("index.html")
    else:
        return render_template("react_redirect.html")


### Challenge Section 1
# Challenge section 1: shows the concert tickets page.
@app.route("/concert", methods=["GET"])
def get_concert_page():
    # Display concert tickets page
    if frontend == "vanilla":
        return render_template("concert.html")
    else:
        return render_template("react_redirect.html")


@app.route("/setup-concert-page", methods=["GET"])
def setup_concert_page():
    try:
        # returns config information that is used by the client JavaScript to display the page.
        return jsonify(
            {
                "basePrice": configInfo["checkout_base_price"],
                "currency": configInfo["checkout_currency"],
            }
        )
    except Exception as e:
        return jsonify(error=str(e)), 403


# Page display after user buy concert tickets
@app.route("/concert-success", methods=["GET"])
def get_concert_success_page():
    # Display concert success page
    if frontend == "vanilla":
        return render_template("concert-success.html")
    else:
        return render_template("react_redirect.html")


### Challenge Section 2
# Challenge section 2: shows the videos purchase page.
@app.route("/videos", methods=["GET"])
def get_video_page():
    # Display checkout page
    if frontend == "vanilla":
        return render_template("videos.html")
    else:
        return render_template("react_redirect.html")


###
# Challenge section 2: returns config information that is used by the client JavaScript
# to display the videos page.
@app.route("/setup-video-page", methods=["GET"])
def setup_video_store():
    try:
        # returns config information that is used by the client JavaScript to display the page.
        return jsonify(
            {
                "discountFactor": configInfo["video_discount_factor"],
                "minItemsForDiscount": configInfo["video_min_items_for_discount"],
                "items": courseInfo,
            }
        )
    except Exception as e:
        return jsonify(error=str(e)), 403


def get_stripe_customer(customer_email):
    response = stripe.Customer.list(email=customer_email)
    if len(response.data):
        return True, response.data[0]
    else:
        return False, None


def create_payment_method(token):
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "token": token["id"]
            }
        )
        return payment_method, None
    except Exception as e:
        return None, e


def create_stripe_customer(name, email, date_time, payment_method_id):
    try:
        new_customer = stripe.Customer.create(
            name=name,
            email=email,
            payment_method=payment_method_id,
            metadata={
                "first_lesson": date_time
            }
        )
        return new_customer, None
    except Exception as e:
        return None, e


### Challenge Section 3
# Challenge section 3: shows the lesson sign up page.
@app.route("/lessons", methods=["GET", "POST"])
def get_lesson_page():
    if request.method == "GET":
        # Display lesson signup
        if frontend == "vanilla":
            return render_template("lessons.html")
        else:
            return render_template("react_redirect.html")
    else:
        email = request.json["email"]
        name = request.json["name"]
        date_time = request.json["date_time"]
        token = request.json["token"]
        customer_valid, customer_info = get_stripe_customer(email)
        if customer_valid:
            return jsonify(
                {
                    "error": {
                        "code": "CUSTOMER_VALID_ERROR",
                        "email": customer_info.email,
                        "cus_id": customer_info.id
                    }
                }
            ), 403
        else:
            payment_method, payment_method_error = create_payment_method(token)
            if payment_method:
                new_customer, customer_error = create_stripe_customer(
                    name, email, date_time, payment_method.id
                )
                if new_customer:
                    return jsonify(
                        {
                            "customer": {
                                "email": email,
                                "cus_id": new_customer.id
                            }
                        }
                    )
                else:
                    return jsonify(
                        {
                            "error": {
                                "code": customer_error.error.code,
                                "message": customer_error.error.message
                            }
                        }
                    ), 403
            else:
                return jsonify(
                    {
                        "error": {
                            "code": payment_method_error.error.code,
                            "message": payment_method_error.error.message
                        }
                    }
                ), 403


def retrieve_customer_payment(customer_id):
    try:
        payment_method = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )
        return payment_method.data[0], None
    except Exception as e:
        return None, e


# Challenge section 4: '/schedule-lesson'
# Authorize a payment for a lesson
#
# Parameters:
# customer_id: id of the customer
# amount: amount of the lesson in cents
# description: a description of this lesson
#
# Example call:
# curl -X POST http://localhost:4242/schdeule-lesson \
#  -d customer_id=cus_GlY8vzEaWTFmps \
#  -d amount=4500 \
#  -d description="Lesson on Feb 25th"
#
# Returns: a JSON response of one of the following forms:
# For a successful payment, return the payment intent:
#   {
#        payment: <payment_intent>
#    }
#
# For errors:
#  {
#    error:
#       code: the code returned from the Stripe error if there was one
#       message: the message returned from the Stripe error. if no payment method was
#         found for that customer return an msg "no payment methods found for <customer_id>"
#    payment_intent_id: if a payment intent was created but not successfully authorized
# }
@app.route("/schedule-lesson", methods=["POST"])
def schdeule_lesson():
    customer_id = request.form["customer_id"]
    amount = request.form["amount"]
    description = request.form["description"]

    customer_payment, e = retrieve_customer_payment(customer_id)
    if customer_payment:
        payment_method_id = customer_payment.id
    else:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message
                }
            }
        ), 403

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            customer=customer_id,
            payment_method=payment_method_id,
            description=description,
            confirmation_method="manual",
            capture_method="manual",
            confirm=True,
            metadata={
                "type": "lessons-payment"
            }
        )
        return jsonify(
            {
                "payment": payment_intent
            }
        )
    except Exception as e:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message,
                    "payment_intent_id": e.error.payment_intent
                }
            }
        ), 403


# Challenge section 4: '/complete-lesson-payment'
# Capture a payment for a lesson.
#
# Parameters:
# amount: (optional) amount to capture if different than the original amount authorized
#
# Example call:
# curl -X POST http://localhost:4242/complete_lesson_payment \
#  -d payment_intent_id=pi_XXX \
#  -d amount=4500
#
# Returns: a JSON response of one of the following forms:
#
# For a successful payment, return the payment intent:
#   {
#        payment: <payment_intent>
#    }
#
# for errors:
#  {
#    error:
#       code: the code returned from the error
#       message: the message returned from the error from Stripe
# }
#
@app.route("/complete-lesson-payment", methods=["POST"])
def complete_lesson_payment():
    payment_intent_id = request.form["payment_intent_id"]
    amount = request.form.get("amount", None)

    try:
        if amount:
            payment_intent = stripe.PaymentIntent.capture(
                payment_intent_id,
                amount_to_capture=amount
            )
        else:
            payment_intent = stripe.PaymentIntent.capture(
                payment_intent_id
            )
        return jsonify(
            {
                "payment": payment_intent
            }
        )
    except Exception as e:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message
                }
            }
        ), 403


# Challenge section 4: '/refund-lesson'
# Refunds a lesson payment.  Refund the payment from the customer (or cancel the auth
# if a payment hasn't occurred).
# Sets the refund reason to 'requested_by_customer'
#
# Parameters:
# payment_intent_id: the payment intent to refund
# amount: (optional) amount to refund if different than the original payment
#
# Example call:
# curl -X POST http://localhost:4242/refund-lesson \
#   -d payment_intent_id=pi_XXX \
#   -d amount=2500
#
# Returns
# If the refund is successfully created returns a JSON response of the format:
#
# {
#   refund: refund.id
# }
#
# If there was an error:
#  {
#    error: {
#        code: e.error.code,
#        message: e.error.message
#      }
#  }
@app.route("/refund-lesson", methods=["POST"])
def refund_lesson():
    payment_intent_id = request.form["payment_intent_id"]
    amount = request.form.get("amount", None)

    try:
        if amount:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount
            )
        else:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id
            )
        return jsonify(
            {
                "refund": refund.id
            }
        )
    except Exception as e:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message
                }
            }
        ), 403


### Challenge Section 5
# Displays the account update page for a given customer
@app.route("/account-update/<customer_id>", methods=["GET"])
def get_account_page(customer_id):
    # Display account update page
    if frontend == "vanilla":
        return render_template("account-update.html")
    else:
        return render_template("react_redirect.html")


# Challenge section 5: '/delete-account'
# Deletes a customer object if there are no uncaptured payment intents for them.
#
# Parameters:
#   customer_id: the id of the customer to delete
#
# Example request
#   curl -X POST http://localhost:4242/delete-account \
#    -d customer_id=cusXXX
#
# Returns 1 of 3 responses:
# If the customer had no uncaptured charges and was successfully deleted returns the response:
#   {
#        deleted: true
#   }
#
# If the customer had uncaptured payment intents, return a list of the payment intent ids:
#   {
#     uncaptured_payments: ids of any uncaptured payment intents
#   }
#
# If there was an error:
#  {
#    error: {
#        code: e.error.code,
#        message: e.error.message
#      }
#  }
#
@app.route("/delete-account/<customer_id>", methods=["POST"])
def delete_account():
    return 0


def get_lesson_payments():
    start_date = datetime.today() - timedelta(days=7)
    start_time = int(time.mktime(start_date.timetuple()))
    payment_list = {"has_more": True}
    starting_after = ""
    lesson_payments = []

    while payment_list["has_more"]:
        try:
            if starting_after:
                payment_list = stripe.PaymentIntent.list(
                    created={
                        "gte": start_time
                    },
                    starting_after=starting_after
                )
            else:
                payment_list = stripe.PaymentIntent.list(
                    created={
                        "gte": start_time
                    }
                )
        except Exception as e:
            return None, e

        if payment_list["data"]:
            for item in payment_list["data"]:
                if item["metadata"] and item["metadata"]["type"] == "lessons-payment":
                    lesson_payments.append(item)

            list_length = len(payment_list["data"])
            starting_after = payment_list["data"][list_length - 1]["id"]

    return lesson_payments, None


# Challenge section 6: '/calculate-lesson-total'
# Returns the total amounts for payments for lessons, ignoring payments
# for videos and concert tickets.
#
# Example call: curl -X GET http://localhost:4242/calculate-lesson-total
#
# Returns a JSON response of the format:
# {
#      payment_total: total before fees and refunds (including disputes), and excluding payments
#         that haven't yet been captured.
#         This should be equivalent to net + fee totals.
#      fee_total: total amount in fees that the store has paid to Stripe
#      net_total: net amount the store has earned from the payments.
# }
#
@app.route("/calculate-lesson-total", methods=["GET"])
def calculate_lesson_total():
    lesson_payments, e = get_lesson_payments()
    if e:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message
                }
            }
        ), 403

    payment_total = 0
    fee_total = 0
    for item in lesson_payments:
        if item["status"] == "succeeded":
            charge_data = item["charges"]["data"][0]
            payment_total += (charge_data["amount"] - charge_data["amount_refunded"])

            if charge_data["application_fee_amount"]:
                fee_total += charge_data["application_fee_amount"]

    net_total = payment_total - fee_total

    return jsonify(
        {
            "payment_total": payment_total,
            "fee_total": fee_total,
            "net_total": net_total
        }
    )


def retrieve_customer(customer_id):
    try:
        customer = stripe.Customer.retrieve(customer_id)
        return customer, None
    except Exception as e:
        return None, e


# Challenge section 6: '/find-customers-with-failed-payments'
# Returns any customer who meets the following conditions:
# The last attempt to make a payment for that customer failed.
# The payment method associated with that customer is the same payment method used
# for the failed payment, in other words, the customer has not yet supplied a new payment method.
#
# Example request: curl -X GET http://localhost:4242/find-customers-with-failed-payments
#
# Returns a JSON response with information about each customer identified and their associated last payment
# attempt and, info about the payment method on file.
# {
#   <customer_id>:
#     customer: {
#       email: customer.email,
#       name: customer.name,
#     },
#     payment_intent: {
#       created: created timestamp for the payment intent
#       description: description from the payment intent
#       status: the status of the payment intent
#       error: the error returned from the payment attempt
#     },
#     payment_method: {
#       last4: last four of the card stored on the customer
#       brand: brand of the card stored on the customer
#     }
#   },
#   <customer_id>: {},
#   <customer_id>: {},
# }
#
@app.route("/find-customers-with-failed-payments", methods=["GET"])
def find_customers():
    lesson_payments, e = get_lesson_payments()
    if e:
        return jsonify(
            {
                "error": {
                    "code": e.error.code,
                    "message": e.error.message
                }
            }
        ), 403

    failed_payments = []
    for lesson_payment in lesson_payments:
        if lesson_payment["last_payment_error"]:
            is_last_payment = True

            for failed_payment in failed_payments:
                if failed_payment["customer"] == lesson_payment["customer"]:
                    is_last_payment = False

            if is_last_payment:
                failed_payments.append(lesson_payment)

    failed_customers_info = []
    for failed_payment in failed_payments:
        customer_id = failed_payment["customer"]

        customer, e = retrieve_customer(customer_id)
        if e:
            return jsonify(
                {
                    "error": {
                        "code": e.error.code,
                        "message": e.error.message
                    }
                }
            ), 403

        customer_payment, e = retrieve_customer_payment(customer_id)
        if e:
            return jsonify(
                {
                    "error": {
                        "code": e.error.code,
                        "message": e.error.message
                    }
                }
            ), 403

        customer_info = {
            customer_id: {
                "customer": {
                    "email": customer["email"],
                    "name": customer["name"]
                },
                "payment_intent": {
                    "created": failed_payment["created"],
                    "description": failed_payment["description"],
                    "status": failed_payment["status"],
                    "error": failed_payment["last_payment_error"],
                },
                "payment_method": {
                    "last4": customer_payment["card"]["last4"],
                    "brand": customer_payment["card"]["brand"]
                },
            }
        }
        failed_customers_info.append(customer_info)

    return jsonify(failed_customers_info)


if __name__ == "__main__":
    app.run()
