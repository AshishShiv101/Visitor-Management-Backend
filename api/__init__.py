from flask import Flask
from api.lifetime import register_startup_event

def bootstrap(app: Flask):
   register_startup_event(app = app)
   return app