from marshmallow import Schema, exceptions

class ValidationHelper:

    def __init__(self) -> None:
        pass

    def validate_and_extract_data(schema : Schema, data) -> tuple:
        '''common validation function, in case module specific validator is required make it say module/module_name/validation.py '''
        try:
            res = schema.load(data = data)
            return res,None
        except exceptions.ValidationError as e:
            return None,e.messages
        except Exception as e:
            return None,str(e)
    
    def verify_params_existence(self, request_params : dict, params_to_verify : list):
        missing_params = []
        verification_res = True
        for param in params_to_verify:
            if param not in request_params.keys():
                verification_res = False
                missing_params.append(param)

        return {"missing_params" : missing_params, "verification_res" : verification_res} 