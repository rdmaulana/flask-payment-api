from flask import make_response, jsonify

def response_profile(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'user_id': result['user_id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'address': result['address'],
            'updated_date': result['updated_date']
        }
    })), status_code