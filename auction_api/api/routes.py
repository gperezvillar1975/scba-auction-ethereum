from flask import Response, json, request, abort, jsonify, session
from pymongo import MongoClient
import pprint
from werkzeug.wrappers import response
from utils import globales
import api.auction_methods as auction_methods
import api.bidder_methods as bidder_methods
import api.bidder_admin as bidder_admin

def get_routes(app):
###
# STATUS
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
###
# AUCTION
###

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
###
# BIDDER
###

    @app.route("/bidder/inscription_request", methods=["POST"])
    def bidder_request():
        res = bidder_methods.bidder_request(request.get_data())
        return res

###
# BIDDER ADMIN
###

    @app.route("/bidder_admin/requests", methods=["GET"])
    def requests_by_status():
        res = bidder_admin.get_requests_by_status(request.args.get('status'))
        return res

    