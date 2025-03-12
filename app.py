from flask import Flask
from flask_cors import CORS
from api import bootstrap
from api.application import flask_app

def main() -> Flask:
    app = flask_app()  # Initialize Flask app
    CORS(app)  # Enable CORS
    return bootstrap(app)  # Perform additional setup

if __name__ == '__main__':
    app = main()
    app.run(debug=True)
