from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


# create new user with data from form
@users_blueprint.route("/", methods=['POST'])
def user_create():
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
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass



    