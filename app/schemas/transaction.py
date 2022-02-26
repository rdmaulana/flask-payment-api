from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

payment_schema = {
    "type": "object",
    "properties": {
        "payment_id": {
            "type": "string"
        },
        "amount": {
            "type": "integer"
        },
        "remarks": {
            "type": "string"
        },
        "balance_before": {
            "type": "integer"
        },
        "balance_after": {
            "type": "integer"
        },
        "created_date": {
            "type": "string"
        },
    },
    "required": ["amount", "remarks"],
    "additionalProperties": False
}

def validate_payment(data):
    try:
        validate(data, payment_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

topup_schema = {
    "type": "object",
    "properties": {
        "top_up_id": {
            "type": "string"
        },
        "user_id": {
            "type": "string"
        },
        "amount": {
            "type": "integer"
        },
        "amount_top_up": {
            "type": "integer"
        },
        "balance_before": {
            "type": "integer"
        },
        "balance_after": {
            "type": "integer"
        },
        "created_date": {
            "type": "string"
        },
    },
    "required": ["amount",],
    "additionalProperties": False
}

def validate_topup(data):
    try:
        validate(data, topup_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

transfer_schema = {
    "type": "object",
    "properties": {
        "transfer_id": {
            "type": "string"
        },
        "from_user_id": {
            "type": "string"
        },
        "target_user": {
            "type": "string"
        },
        "amount": {
            "type": "integer"
        },
        "remarks": {
            "type": "string"
        },
        "balance_before": {
            "type": "integer"
        },
        "balance_after": {
            "type": "integer"
        },
        "created_date": {
            "type": "string"
        },
    },
    "required": ["target_user", "amount", "remarks"],
    "additionalProperties": False
}

def validate_transfer(data):
    try:
        validate(data, transfer_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}