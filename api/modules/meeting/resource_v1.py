from flask_restful import Resource
from flask import request
from api.utils.response import ApiResponse
import api.utils.http_status as status
from api.modules.meeting.helper_v1 import MeetingHelper
from api.utils.validation import ValidationHelper
from db.base import db

MEETING_ENDPOINT = "/meeting"

class meetingResource(Resource):

    def __init__(self) -> None :
        self.response_helper = ApiResponse()
        self.resource_helper = MeetingHelper()
        self.validation_helper = ValidationHelper()

    def get(self):
        ''' As of the current implementation, all meetings are returned at once as response if meeting_date not provided, needs to be improved with paginated requests'''

        request_params = request.args.to_dict()

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['_action']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide an action to perform", resp_code = 1001)

        request_map = self.resource_helper.initialize_resource_action_map(request_type = "get")

        if not self.resource_helper.validate_action(request_params = request_params, request_map = request_map):
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide a valid action to perform", resp_code = 1001)
        
        return request_map[request_params['_action']](request_params = request_params)
    
    def post(self):
        request_params = request.args.to_dict()

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['_action']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide an action to perform", resp_code = 1001)

        request_map = self.resource_helper.initialize_resource_action_map(request_type = "post")

        if not self.resource_helper.validate_action(request_params = request_params, request_map = request_map):
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide a valid action to perform", resp_code = 1001)
        
        return request_map[request_params['_action']](request_params = request_params)

    def patch(self):
        request_params = request.args.to_dict()

        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['_action']).get('verification_res') == False:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide an action to perform", resp_code = 1001)

        request_map = self.resource_helper.initialize_resource_action_map(request_type = "patch")

        if not self.resource_helper.validate_action(request_params = request_params, request_map = request_map):
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Please provide a valid action to perform", resp_code = 1001)
        
        return request_map[request_params['_action']](request_params = request_params)
    
    def delete(self):
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Method not allowed", resp_code = 1001)
    
    def put(self):
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Method not allowed", resp_code = 1001)