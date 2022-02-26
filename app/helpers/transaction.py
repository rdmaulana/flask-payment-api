from flask import make_response, jsonify

def response_topup(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'top_up_id': result['top_up_id'],
            'amount_top_up': result['amount_top_up'],
            'balance_before': result['balance_before'],
            'balance_after': result['balance_after'],
            'created_date': result['created_date']
        }
    })), status_code

def response_payment(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'payment_id': result['payment_id'],
            'amount': result['amount'],
            'remarks': result['remarks'],
            'balance_before': result['balance_before'],
            'balance_after': result['balance_after'],
            'created_date': result['created_date']
        }
    })), status_code

def response_transfer(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'transfer_id': result['transfer_id'],
            'amount': result['amount'],
            'remarks': result['remarks'],
            'balance_before': result['balance_before'],
            'balance_after': result['balance_after'],
            'created_date': result['created_date']
        }
    })), status_code

def response_history_transaction(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': result
    })), status_code