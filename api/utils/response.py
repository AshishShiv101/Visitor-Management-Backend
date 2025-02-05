from typing import Any
import api.utils.http_status as status
class ApiResponse:

    def __verify_faliure(self, code : int):
        return (status.is_client_error(code = code) or status.is_server_error(code = code))

    def response(self, code : int, data : Any = {}, **kwargs):
        success : bool = kwargs.pop("success", not(self.__verify_faliure(code = code)))
        message : str = kwargs.pop("message", "ok")
        resp_code : int = kwargs.pop("resp_code", 1001)

        response_body : dict = {
            "success" : success,
            "message" : message,
            "data" : data,
            "resp_code" : resp_code,
            "extras" : kwargs
        }

        return response_body, code