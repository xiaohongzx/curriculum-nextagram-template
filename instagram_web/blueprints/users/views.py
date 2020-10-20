from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
from helpers import upload_to_s3


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
def show(username):
    user = User.get_or_none(User.username == username)
    return render_template("users/show.html", user = user)

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    #user = User.get_by_id(id)
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id ==  user.id:
            return render_template('users/edit.html', id = id, user = user)
        else:
            return "Unauthorized to view others profile page"
    else:
        return "No such user found !"


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):

    # user = User.get_by_id(id)
    # data = request.form
    # update_user = User.update(username = data.get('username'),email = data.get('email')).where(User.id == id)
    # if update_user.execute():
    #     flash("changed")
    #     return redirect(url_for('users.edit', id=current_user.id))
    # else:
    #     flash("something wrong")
    #     return redirect(url_for('users.edit', id=current_user.id))

    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id ==  user.id:
            data = request.form
            hashed_password = user.password_hash
            result = check_password_hash(hashed_password, data.get('old_password'))
            if result:
                user.username = data.get("username")
                user.email = data.get("email")

                if data.get("password") != "":
                    user.password = data.get("password")

                if user.save():
                    return redirect(url_for("users.show", id = id, username = user.username))
                else:
                    return redirect(url_for("users.edit", id = id))

            else:
                flash("Wrong comfirmation password")
                return redirect(url_for("users.edit",id = id))
        else:
            return "Unauthorized to view others profile page"
    else:
        return "No such user found !"


@users_blueprint.route('/<id>/upload_profile', methods=['POST'])
@login_required
def upload_profile(id):
    user = User.get_or_none(User.id == id)
    if user:
        if "profile_image" not in request.files:
            return "No user_file key in request.files"

        file = request.files["profile_image"]

        if file.filename == "":
            return "Please select a file"
        
        if file:
            file_path = upload_to_s3(file)
            user.image_path = file_path
            if user.save():
                return redirect(url_for('users.show', username = user.username))
            else:
                return "Could not upload profile image, please go back and try again"
        
        else:
            return redirect(url_for('users.edit', id=id))
    else:
        return "No such User"

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# def allowed_file(filename):
#     return '.' in filename and \
#             filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# @users_blueprint.route('/profile_image')
# def profile_image():
#     return render_template('users/profile_pic.html')


# @users_blueprint.route('/profile_image/upload', methods=["POST"])
# def upload_file():
#     file = request.files["user_file"]  

#     if file.filename == "":
#         return "Please select an image"

#     if file:
#         output = upload_file_to_s3(file, S3_BUCKET)
#         return str(output)
#     else:
#         return redirect(url_for('users.profile_image'))