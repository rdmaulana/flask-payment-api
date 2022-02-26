from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

update_profile_schema = {
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
        "address": {
            "type": "string"
        },
        "updated_date": {
            "type": "string"
        },
    },
    "required": [],
    "additionalProperties": False
}

def validate_profile_update(data):
    try:
        validate(data, update_profile_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}