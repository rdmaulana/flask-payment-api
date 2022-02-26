from datetime import datetime
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app import app, mongo, bcrypt, jwt
from app.schemas.user import validate_user

from app.helpers.user import ( 
    response_auth_register, 
    response_error_auth_register,
    response_auth_login
)

auth = Blueprint('auth', __name__)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

@auth.route("/", methods=["GET"])
@jwt_required()
def index():
    return get_jwt_identity()

@auth.route("/register", methods=["POST"])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data['user_id'] = str(uuid.uuid4())
        data['balance'] = 0
        check_user = mongo.db.users.find_one({'phone_number': data['phone_number']}, {"_id": 0})
        if not check_user:
            mongo.db.users.insert_one(data)
            return response_auth_register('SUCCESS', data, 200)
        return jsonify({"message": "Phone number already registered"})
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@auth.route("/login", methods=["POST"])
def login():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'phone_number': data['phone_number']})
        if user and data['pin'] == user['pin']:
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return response_auth_login('SUCCESS', user, 200)
        else:
            return jsonify({'message': 'Phone number and pin doesn’t match'}), 401
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'status': 'SUCCESS', 'result': ret}), 200