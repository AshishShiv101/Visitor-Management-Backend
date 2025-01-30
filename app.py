from flask import Flask
from api import bootstrap
from db.models import * 
from api.application import flask_app

def main() -> Flask:
    return bootstrap(app = flask_app())

if __name__ == '__main__':
    app = main()
    app.run(debug = True)