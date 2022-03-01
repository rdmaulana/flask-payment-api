from app import mongo, create_app
from app.tasks import celery

@celery.task
def transfer_process(payload):
    flask_app = create_app()
    with flask_app.app_context():
        get_target_user = mongo.db.users.find_one({'user_id': payload['target_user']})
        try:
            transfer = mongo.db.transactions.insert_one(payload)
            if transfer:
                mongo.db.users.update_one(
                    {'user_id': payload['from_user_id']},
                    {'$set': {'balance': payload['balance_after']}}
                ) 
                mongo.db.users.update_one(
                    {'user_id': payload['target_user']},
                    {'$set': {'balance': get_target_user['balance'] + payload['amount']}}
                )
                return {'message': 'SUCCESS'}
            return {'message': 'FAILED'}
        except Exception as e:
            return {'message': 'FAILED', 'details': str(e)}