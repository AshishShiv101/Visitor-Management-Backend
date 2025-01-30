from flask import Flask, jsonify

def register_routes(app: Flask):
    @app.route("/ping")
    def health():
        return jsonify({"status": "ok", "message": "pong"}), 200