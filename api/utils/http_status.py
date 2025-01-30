def is_client_error(code : int):
    return code >= 400 and code <= 499

def is_server_error(code : int):
    return code >= 500 and code <= 599

HTTP_200_OK = 200