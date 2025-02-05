from flask import Blueprint
from flask_restful import Api
from api.modules.auth.resource_v1 import AuthResource, AUTH_ENDPOINT
from api.modules.user.resource_v1 import UserResource, USER_ENDPOINT

def api_v1():
    v1_blueprint = Blueprint("v1_blueprint", __name__)
    v1_api = Api(v1_blueprint)

    v1_api.add_resource(AuthResource, AUTH_ENDPOINT)
    v1_api.add_resource(UserResource, USER_ENDPOINT)
    return v1_blueprint