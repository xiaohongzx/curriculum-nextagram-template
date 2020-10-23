from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from helpers import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=[ 'POST' ])
def create():

    data = request.form
    user = User.get_or_none(username= data.get('username'))

    if user:
        hashed_password = user.password_hash # password hash stored in database for a specific user
        result = check_password_hash(hashed_password, data.get('password')) # what is result? Test it in Flask shell and implement it in your view function!

        if result:
           # session["user_id"] = user.id
            login_user(user)
            flash("Login successfully")
            return redirect(url_for('users.show',username = user.username))
        else:
            flash("Wrong password")
            return redirect(url_for('sessions.new'))
    else:
        flash("USer not found")
        return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/delete', methods=['POST'])
def destroy():
    logout_user()
    flash('Signout')
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route("/google_login", methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google", methods=['GET'])
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Login Succesfully.")
        return redirect(url_for('users.show',username = user.username))
    else:
        flash("No such user with this email  detected. Please sign up an account with this email first!")
        return redirect(url_for('users.new'))

