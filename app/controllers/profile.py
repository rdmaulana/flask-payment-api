from datetime import datetime
from flask import Blueprint, jsonify, request
from app import app, mongo
from app.helpers.profile import response_profile
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity
from app.schemas.profile import validate_profile_update

profile = Blueprint('profile', __name__)

@profile.route('/', methods=["PUT"])
@jwt_required()
def profile_update():
    user = get_jwt_identity()
    get_user = mongo.db.users.find_one({'phone_number': user['phone_number']})
    data = validate_profile_update(request.get_json())
    if data['ok']:
        data = data['data']
        data['user_id'] = get_user['user_id']
        data['updated_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        try:
            mongo.db.users.update_one({'user_id': data['user_id']}, {'$set': data})
        except Exception as e:
            print(e)
        return response_profile('SUCCESS', data, 200)
    return jsonify({'message': 'unauthenticated'}), 401


