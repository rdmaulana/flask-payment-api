from app import app
from app.helpers.user import response

@app.errorhandler(404)
def route_not_found(e):
    return response(
        'failed', 
        'Endpoint not found', 
        404
    )

@app.errorhandler(405)
def method_not_found(e):
    return response(
        'failed',
        'The method is not allowed for the requested URL', 
        405
    )

@app.errorhandler(500)
def internal_server_error(e):
    return response(
        'failed',
        'Internal serve error',
        500
    )