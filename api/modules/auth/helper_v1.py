import jwt
import datetime
from api.utils.response import ApiResponse
import api.utils.http_status as status
from db.models.users_model import Users
from db.models.roles_model import Roles
from settings import Settings

class AuthHelper:
    
    def __init__(self) -> None :
        self.response_helper = ApiResponse()

    def initialize_resource_action_map(self, request_type : str):
        resource_action_map = None

        if request_type == 'post':
            resource_action_map = {
                'login_user' : self.handle_login
            }

        return resource_action_map

    def verify_params_existence(self, request_params : dict, params_to_verify : list):
        missing_params = []
        verification_res = True
        for param in params_to_verify:
            if param not in request_params.keys():
                verification_res = False
                missing_params.append(param)

        return {"missing_params" : missing_params, "verification_res" : verification_res}
    
    def validate_action(self, request_params : dict, request_map : dict):
        return request_params.get('_action') in request_map.keys()
    
    def _generate_token(self, token_payload : dict):
        return jwt.encode(token_payload, Settings.SECRET_KEY, algorithm='HS256')

    def handle_login(self, request_params : dict):

        param_verification_res = self.verify_params_existence(request_params = request_params, params_to_verify = ['phno', 'password'])

        if param_verification_res.get("verification_res") == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = f"Insufficient details, can't attempt login", data = {"missing_params" : param_verification_res.get("missing_params")}, resp_code = 1001)
        
        existing_user = Users.query.filter_by(phno = request_params.get('phno'), password = request_params.get('password')).first()

        if not existing_user:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User does not exist", resp_code = 1001)
        
        user_role = Roles.query.filter_by(id=existing_user.role_id).first()

        if not user_role:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User does not have a role, DB inconsistency!", resp_code = 1001)

        token_payload = {
                'username': existing_user.user_name,
                'phno': existing_user.phno,
                'role' : user_role.role.value,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
        }

        token = self._generate_token(token_payload = token_payload)
        return self.response_helper.response( code = status.HTTP_200_OK, message = "Logged in successfully!", data = {'token' : token}, resp_code = 1001)