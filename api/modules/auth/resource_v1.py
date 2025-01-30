from flask_restful import Resource
from flask import request
from api.utils.response import ApiResponse
import api.utils.http_status as status
from api.modules.auth.helper_v1 import AuthHelper
from db.base import db

AUTH_ENDPOINT = "/auth"

class AuthResource(Resource):

    def __init__(self) -> None :
        self.response_helper = ApiResponse()
        self.resource_helper = AuthHelper()

    def post(self):
        request_params = request.args.to_dict()

        if self.resource_helper.verify_params_existence(request_params = request_params, params_to_verify = ["_action"]).get('verification_res') == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "Please provide an action to perform", resp_code = 1001)
        
        request_map = self.resource_helper.initialize_resource_action_map(request_type = 'post')

        if not self.resource_helper.validate_action(request_params = request_params, request_map = request_map):
            return self.response_helper.response( code = status.HTTP_200_OK, message = "Please provide a valid action to perform", resp_code = 1001)

        return request_map[request_params['_action']](request_params = request_params)