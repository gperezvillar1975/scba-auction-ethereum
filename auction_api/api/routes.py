from flask import Response, json, request, abort, jsonify, session
from pymongo import MongoClient
import pprint
from werkzeug.wrappers import response
from utils import globales
import api.auction_methods as auction_methods

def get_routes(app):
###
# Rutas definidas para status, importa las funciones de api.status (/api/status.py)
###
    @app.route("/status/ping", methods=["GET"])
    def get_ping():
        
        return jsonify("pong")
    
    @app.route("/status/ready", methods=["GET"])
    def get_ready():
        try:
            mg=MongoClient(globales.mongodb_uri)
            mg.admin.command("ping")
            return jsonify("DB Connection OK .... Ready")
        except:
            return jsonify("DB Connection FAIL .... NOT Ready")

    @app.route("/auction/auction", methods=["POST"])
    def auction_post():
        res = auction_methods.auction_post(request.get_data())
        return res
    @app.route("/auction/auction", methods=["GET"])
    def auction_get():
        res = auction_methods.auction_get(request.args.get('code'))
        return res
    @app.route("/auction/auction", methods=["DELETE"])
    def auction_delete():
        res = auction_methods.auction_delete(request.args.get('code'))
        return res