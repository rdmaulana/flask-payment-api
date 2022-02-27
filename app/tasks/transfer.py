import uuid
from datetime import datetime
from flask import jsonify, make_response
from app import mongo, create_app
from app.helpers.transaction import response_transfer
from app.schemas.transaction import validate_transfer
from app.tasks import celery

@celery.task
def transfer_process(user, payload):
    flask_app = create_app()
    with flask_app.app_context():
        get_user = mongo.db.users.find_one({'phone_number': user['phone_number']})

        data = validate_transfer(payload)
        if data['ok']:
            data = data['data']
            data['transfer_id'] = str(uuid.uuid4())
            data['from_user_id'] = get_user['user_id']
            data['balance_before'] = get_user['balance']
            data['balance_after'] = data['balance_before'] - data['amount']
            data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            get_target_user = mongo.db.users.find_one({'user_id': data['target_user']})

            if get_user['balance'] >= data['amount']:
                try:
                    transfer = mongo.db.transactions.insert_one(data)
                    if transfer:
                        mongo.db.users.update_one(
                            {'user_id': get_user['user_id']},
                            {'$set': {'balance': data['balance_after']}}
                        ) 
                        mongo.db.users.update_one(
                            {'user_id': data['target_user']},
                            {'$set': {'balance': get_target_user['balance'] + data['amount']}}
                        )
                except Exception as e:
                    print(e)
                # return response_transfer('SUCCESS', data, 200)
                return {'message': 'SUCCESS'}
            # return make_response(jsonify({'message': 'Balance is not enough'})), 400
            return {'message': 'FAILED'}
        # return make_response(jsonify({'message': 'Unauthenticated'})), 401
        return {'message': 'FAILED'}