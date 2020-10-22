from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models.user import User
from models.image import Image
from models.transaction import Transaction
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from helpers import get_client_token, create_transaction
from braintree.successful_result import SuccessfulResult
import requests

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')


@transactions_blueprint.route('/new', methods=['GET'])
def new(image_id):
    print(image_id)
    return render_template('transactions/new.html', client_token = get_client_token(), image_id=image_id)

@transactions_blueprint.route('/', methods=['POST'])
def create(image_id):
    data = request.form
    image = Image.get_by_id(image_id)
    result = create_transaction(data.get("amount"),data.get("payment_method_nonce"))
    if type(result) == SuccessfulResult:
        new_transaction = Transaction(amount = data.get("amount"), image=image, user_id= current_user.id )
        if new_transaction.save():
            requests.post(
                "https://api.mailgun.net/v3/sandboxf2ff5a19c3874580ac009024f05edf38.mailgun.org/messages",
                auth=("api", "17b5f5ca8aa9f463dab52b23c72c4c9d-53c13666-50ef3ea2"),
                data={"from": "Mailgun Sandbox <postmaster@sandboxf2ff5a19c3874580ac009024f05edf38.mailgun.org>",
                    "to": "hongxhong92@gmail.com <hongxhong92@gmail.com>",
                    "subject": "Hello hongxhong92@gmail.com",
                    "text": "Succesfully receive a donation"})

            return redirect(url_for("users.show",username = image.user.username))
        else:
            return "Could not save transaction"
    else:
        return "Could not create braintree transaction"

    return redirect(url_for("users.show", username = image.user.username))
