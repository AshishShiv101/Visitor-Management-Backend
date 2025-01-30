from flask import Flask
from db import init_database
from api.routes import register_routes

def register_startup_event(app: Flask):
    """
    Actions to be performed on Application Startup
    """
    register_routes(app = app)
    init_database(app)