from flask import Flask, jsonify
from api.routes.v1 import api_v1

def register_routes(app: Flask):
    @app.route("/ping")
    def health():
        return jsonify({"status": "ok", "message": "pong"}), 200
    
    app.register_blueprint(api_v1(), url_prefix="/api/v1")