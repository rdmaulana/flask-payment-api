from crypt import methods
from datetime import datetime
import uuid
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import app, mongo, q
from app.schemas.transaction import validate_topup, validate_payment, validate_transfer
from app.helpers.transaction import (
    response_topup, 
    response_payment, 
    response_transfer,
    response_history_transaction
)

transaction = Blueprint('transaction', __name__)

@transaction.route('/', methods=["GET"])
@jwt_required()
def history_transactions():
    user = get_jwt_identity()
    get_user = mongo.db.users.find_one({'phone_number': user['phone_number']})
    transactions = mongo.db.transactions.find({'user_id': get_user['user_id']}, {'_id':0})
    if transactions:
        return response_history_transaction('SUCCESS', list(transactions), 200)
    return jsonify({'Unauthenticated'}), 401

@transaction.route("/topup", methods=["POST"])
@jwt_required()
def topup():
    user = get_jwt_identity()
    get_user = mongo.db.users.find_one({'phone_number': user['phone_number']})
    data = validate_topup(request.get_json())
    if data['ok']:
        data = data['data']
        data['top_up_id'] = str(uuid.uuid4())
        data['user_id'] = get_user['user_id']
        data['amount_top_up'] = data['amount']
        data['balance_before'] = get_user['balance']
        data['balance_after'] = data['balance_before'] + data['amount_top_up']
        data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        try:
            top_up = mongo.db.transactions.insert_one(data)
            if top_up:
                mongo.db.users.update_one(
                    {'user_id': get_user['user_id']},
                    {'$set': {'balance': get_user['balance'] + data['amount']}}
                )
        except Exception as e:
            print(e)
        return response_topup('SUCCESS', data, 200) 
    return jsonify({
        'message': 'Unauthenticated'
    }), 401

@transaction.route("/pay", methods=["POST"])
@jwt_required()
def pay():
    user = get_jwt_identity()
    get_user = mongo.db.users.find_one({'phone_number': user['phone_number']})
    data = validate_payment(request.get_json())
    if data['ok']:
        data = data['data']
        data['payment_id'] = str(uuid.uuid4())
        data['user_id'] = get_user['user_id']
        data['balance_before'] = get_user['balance']
        data['balance_after'] = data['balance_before'] - data['amount']
        data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if get_user['balance'] >= data['amount']:
            try:
                pay_it = mongo.db.transactions.insert_one(data)
                if pay_it:
                    mongo.db.users.update_one(
                        {'user_id': get_user['user_id']},
                        {'$set': {'balance': data['balance_after']}}
                    ) 
            except Exception as e:
                print(e)
            return response_payment('SUCCESS', data, 200)
        return jsonify({'message': 'Balance is not enough'}), 400
    return jsonify({'message': 'Unauthenticated'}), 401

def transfer_process(user, payload):
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
            return response_transfer('SUCCESS', data, 200)
        return jsonify({'message': 'Balance is not enough'}), 400
    return jsonify({'message': 'Unauthenticated'}), 401

@transaction.route("/transfer", methods=["POST"])
@jwt_required()
def transfer():
    from app.controllers.transaction import transfer_process

    user = get_jwt_identity()
    data = request.get_json()
    
    job = q.enqueue_call(
        func=transfer_process, args=(user, data), result_ttl=5000
    )
    if job:
        return jsonify({'message': 'SUCCESS'}), 200
    return jsonify({'message': 'Unauthenticated'}), 401