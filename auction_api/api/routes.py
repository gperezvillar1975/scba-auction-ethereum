from flask import Response, json, request, abort, jsonify, session
from pymongo import MongoClient
import pprint
def get_routes(app):
###
# Rutas definidas para status, importa las funciones de api.status (/api/status.py)
###
    @app.route("/status/ping", methods=["GET"])
    def get_ping():
        
        return jsonify("pong")
    
    @app.route("/status/ready", methods=["GET"])
    def get_ready():
        conn_str = "mongodb://admin:linsm08@mongodb.bus-justicia.org.ar:27017"        
        try:
            mg=MongoClient(conn_str)
            mg.admin.command("ping")
            return jsonify("DB Connection OK .... Ready")
        except:
            return jsonify("DB Connection FAIL .... NOT Ready")

