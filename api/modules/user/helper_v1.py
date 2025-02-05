from api.utils.validation import ValidationHelper
from api.utils.response import ApiResponse
import api.utils.http_status as status
from db.models.users_model import Users
from db.models.roles_model import Roles
from db.base import db
from db.utils.db_enums import RoleEnum

class UserHelper:

    def __init__(self) -> None:
        self.validation_helper = ValidationHelper()
        self.response_helper = ApiResponse()

    def initialize_resource_action_map(self, request_type : str):
        resource_action_map = None

        if request_type == "get":
            resource_action_map = {
                'get_user_details' : self.get_user_details,
                'get_specific_user_details' : self.get_specific_user_details
            }
        elif request_type == "patch":
            resource_action_map = {
                'edit_user_details' : self.edit_user_details
            }
        elif request_type == "delete":
            resource_action_map = {
                'remove_user' : self.remove_user
            }

        return resource_action_map
    
    def validate_action(self, request_params : dict, request_map : dict):
        return request_params.get('_action') in request_map.keys()

    def format_user_details(self, user_details : list) -> list:
        formatted_user_details = []
        for user in user_details:
            user_details = {}
            user_details['user_name'] = user.user_name
            user_details['phno'] = user.phno
            user_role = Roles.query.filter_by(id=user.role_id).first()
            user_details['role'] = user_role.role.value if user_role else None
            formatted_user_details.append(user_details)
        
        return formatted_user_details

    def get_user_details(self, request_params : dict):

        if request_params.get('role', None) is not None:

            if request_params['role'] not in RoleEnum.__members__:
                    return self.response_helper.response(code = status.HTTP_200_OK, message = f'Provided role does not exist!', resp_code = 1001)
            
            role_obj = Roles.query.filter_by(role = request_params['role']).first()
            user_details = Users.query.filter_by(role_id=role_obj.id).all() #need to update this with paginated requests!!

        else:
            user_details = Users.query.all() #need to update this with paginated requests!!

        formatted_user_details = self.format_user_details(user_details = user_details)
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"User details fetched", data = formatted_user_details, resp_code = 2000)

    def get_specific_user_details(self, request_params : dict):

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['phno']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide the user's phno to fetch details", resp_code = 1001)
        
        user_details = Users.query.filter_by(phno = request_params['phno']).first()
        
        if not user_details:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"User with this phno does not exist", resp_code = 1001)

        formatted_user_details = self.format_user_details(user_details = [user_details])
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"user details fetched", data = formatted_user_details, resp_code = 2000)

    def edit_user_details(self, request_params : dict):

        '''this function is not dyanmic, role is updated in a hardcoded way, make it dyanamic if and when need arises'''

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['phno']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide the user's phno to edit details", resp_code = 1001)

        user_details = Users.query.filter_by(phno = request_params['phno']).first()
        
        if not user_details:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"User with this phone number does not exist", resp_code = 1001)

        for key, value in request_params.items():
            if key == "role":  
                
                if value not in RoleEnum.__members__:
                    return self.response_helper.response(code = status.HTTP_200_OK, message = f'Provided role does not exist!', resp_code = 1001)

                role_obj = Roles.query.filter_by(role=value).first()
                user_details.role_id = role_obj.id  

            elif hasattr(user_details, key) and key != "phno":
                setattr(user_details, key, value)

        db.session.commit()
        return self.response_helper.response(code = status.HTTP_200_OK, message = f'All valid user details edited successfully', resp_code = 2000)
    
    def remove_user(self, request_params : dict):

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['phno']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide the user's phno to edit details", resp_code = 1001)

        user_details = Users.query.filter_by(phno = request_params['phno']).first()
        
        if not user_details:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"User with this phone number does not exist", resp_code = 1001)
        
        Users.query.filter_by(phno=request_params['phno']).delete()
        db.session.commit()

        return self.response_helper.response(code = status.HTTP_200_OK, message = f"user removed successfully", resp_code = 2000)