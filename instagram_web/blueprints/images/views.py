from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


