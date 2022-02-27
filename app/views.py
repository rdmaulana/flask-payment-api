from app.helpers.user import response

def bad_request(e):
    '''
    error 404 response
    '''
    return response(
        'failed', 
        'Request data cannot be executable', 
        400
    )

def route_not_found(e):
    '''
    error 404 response
    '''
    return response(
        'failed', 
        'Endpoint not found', 
        404
    )

def method_not_found(e):
    '''
    error 405 response
    '''
    return response(
        'failed',
        'The method is not allowed for the requested URL', 
        405
    )

def internal_server_error(e):
    '''
    error 500 response
    '''
    return response(
        'failed',
        'Internal serve error',
        500
    )