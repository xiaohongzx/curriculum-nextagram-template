from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User


session_blueprint = Blueprint('session',
                            __name__,
                            template_folder='templates')


@session_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('session/login.html')




