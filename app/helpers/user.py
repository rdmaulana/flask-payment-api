from flask import make_response, jsonify

def response(status, message, status_code):
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code

def response_auth_register(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'user_id': result['user_id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'phone_number': result['phone_number'],
            'address': result['address'],
            'created_data': result['created_date']
        }
    })), status_code

def response_error_auth_register(message, status_code):
    return make_response(jsonify({
        'message': message
    })), status_code

def response_auth_login(status, result, status_code):
    return make_response(jsonify({
        'status': status,
        'result': {
            'access_token': result['token'],
            'refresh_token': result['refresh']
        }
    })), status_code