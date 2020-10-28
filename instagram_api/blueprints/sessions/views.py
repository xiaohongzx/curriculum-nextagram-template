from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api',
                             __name__,
                             template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.get_or_none(username= data.get('username'))

    if user:
        hashed_password = user.password_hash # password hash stored in database for a specific user
        result = check_password_hash(hashed_password, data.get('password')) # what is result? Test it in Flask shell and implement it in your view function!

        if result:
           # session["user_id"] = user.id
            token = create_access_token(identity =user.id)
            return jsonify({"token":token})
    return jsonify({"Error": "Invalid credentials"})

