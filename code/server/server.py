#! /usr/bin/env python3.6

"""
server.py
Stripe Card Payments Certification.
Python 3.6 or newer required.
"""

import json
import os

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, find_dotenv

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


### Challenge Section 3
# Challenge section 3: shows the lesson sign up page.
@app.route("/lessons", methods=["GET"])
def get_lesson_page():
    # Display lesson signup
    if frontend == "vanilla":
        return render_template("lessons.html")
    else:
        return render_template("react_redirect.html")


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
def schdeule-lesson():
    return 0


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
    return 0

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
    return 0

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
@app.route("/calculate-lesson-total", methods=["POST"])
def calculate_lesson_total():
    return 0


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
@app.route("/find-customers-with-failed-payments", methods=["POST"])
def find_customers():
    return 1


if __name__ == "__main__":
    app.run()
