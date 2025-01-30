'''common validation function, in case module specific validator is required make it say module/module_name/validation.py '''

from marshmallow import Schema, exceptions

def validate_and_extract_data(schema : Schema, data) -> tuple:
    try:
        res = schema.load(data = data)
        return res,None
    except exceptions.ValidationError as e:
        return None,e.messages
    except Exception as e:
        return None,str(e)