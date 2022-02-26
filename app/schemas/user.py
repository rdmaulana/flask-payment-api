from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string"
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "address": {
            "type": "string"
        },
        "pin": {
            "type": "string"
        },
        "created_date": {
            "type": "string"
        },
        "balance": {
            "type": "integer"
        },
    },
    "required": ["phone_number", "pin"],
    "additionalProperties": False
}

def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}