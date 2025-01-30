from flask import Flask

def flask_app() -> Flask:
    return Flask(__name__)