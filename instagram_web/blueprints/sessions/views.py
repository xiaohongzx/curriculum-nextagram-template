from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


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




