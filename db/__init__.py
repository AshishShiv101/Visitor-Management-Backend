from flask import Flask
from settings import Settings
from db.base import db as database

def init_database(app : Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = str(Settings.DATABASE_URL)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Settings.SQLALCHEMY_TRACK_MODIFICATIONS
    database.init_app(app = app)
    
    if Settings.ALLOW_AUTO_GENERATE_TABLES:
        with app.app_context():
            database.create_all()