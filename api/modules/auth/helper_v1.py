import jwt
import datetime
from api.utils.response import ApiResponse
from api.utils.validation import ValidationHelper
import api.utils.http_status as status
from db.models.users_model import Users
from db.models.roles_model import Roles
from db.utils.db_enums import RoleEnum
from settings import Settings
from werkzeug.security import generate_password_hash, check_password_hash
from db.base import db

class AuthHelper:
    
    def __init__(self) -> None :
        self.response_helper = ApiResponse()
        self. validation_helper = ValidationHelper()

    def initialize_resource_action_map(self, request_type : str):
        resource_action_map = None

        if request_type == 'post':
            resource_action_map = {
                'login_user' : self.handle_login,
                'register_user' : self.handle_user_registration
            }

        return resource_action_map

    def validate_action(self, request_params : dict, request_map : dict):
        return request_params.get('_action') in request_map.keys()
    
    def _generate_token(self, token_payload : dict):
        return jwt.encode(token_payload, Settings.SECRET_KEY, algorithm='HS256')

    def handle_login(self, request_params : dict):

        param_verification_res = self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['phno', 'password'])

        if param_verification_res.get("verification_res") == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = f"Insufficient details, can't attempt login", data = {"missing_params" : param_verification_res.get("missing_params")}, resp_code = 1001)
        
        existing_user = Users.query.filter_by(phno = request_params.get('phno')).first()

        if not existing_user:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User does not exist", resp_code = 1001)
        
        user_role = Roles.query.filter_by(id=existing_user.role_id).first()

        if not user_role:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User does not have a role, DB inconsistency!", resp_code = 1001)
        
        user_password = request_params.get("password")

        if not check_password_hash(existing_user.password, user_password):
            return self.response_helper.response( code = status.HTTP_200_OK, message = "Invalid Password", resp_code = 1001)

        token_payload = {
                'username': existing_user.user_name,
                'phno': existing_user.phno,
                'role' : user_role.role.value,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
        }

        token = self._generate_token(token_payload = token_payload)
        return self.response_helper.response( code = status.HTTP_200_OK, message = "Logged in successfully!", data = {'token' : token}, resp_code = 1001)

    def handle_user_registration(self, request_params : dict): 
        param_verification_res = self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['user_name', 'phno', 'password', 'role'])

        if param_verification_res.get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Insufficient details, can't register user.", data = {"missing_params" : param_verification_res.get('missing_params')}, resp_code = 1001)
        
        existing_user = Users.query.filter_by(phno = request_params.get('phno')).first()

        if existing_user:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this phno already exists", resp_code = 1001)

        user_role = request_params.get('role')

        if user_role not in RoleEnum.__members__:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f'Provided role does not exist!', resp_code = 1001)
        
        
        user_name, phno, password = request_params.get('user_name'), request_params.get('phno'), request_params.get('password')
        role_res = Roles.query.filter_by(role = user_role).first()
        user_role_id = role_res.id

        new_user = Users(user_name = user_name, phno = phno, password = generate_password_hash(password= password), role_id = user_role_id)
        db.session.add(new_user)
        db.session.commit()

        return self.response_helper.response( code = status.HTTP_200_OK, message = f"User registration successful", resp_code = 2000)