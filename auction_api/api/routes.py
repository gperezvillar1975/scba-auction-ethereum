from flask import Response, json, request, abort, jsonify, session
import pprint
def get_routes(app):
###
# Rutas definidas para status, importa las funciones de api.status (/api/status.py)
###
    @app.route("/status/ping", methods=["GET"])
    def get_ping():
        
        return jsonify("pong")
    
