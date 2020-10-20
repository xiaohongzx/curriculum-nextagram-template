from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from flask_login import login_required, current_user, login_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


# create new user with data from form
@users_blueprint.route("/", methods=['POST'])
def create():
    # get form value in form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    create_new_user = User(username = username, email = email, password = password)

    if create_new_user.save():
        return redirect("/")
    else:
        return redirect(url_for("users.new"))

@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    if current_user.is_authenticated:
        print("hey")
        return username
    else:
        return "Please login to continue"

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user ==  user:
        return render_template('users/user_profile.html')
    else:
        return "Unauthorized to view others profile page"


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):

    user = User.get_by_id(id)
    data = request.form
    update_user = User.update(username = data.get('username'),email = data.get('email')).where(User.id == id)
    if update_user.execute():
        flash("changed")
        return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash("something wrong")
        return redirect(url_for('users.edit', id=current_user.id))



    