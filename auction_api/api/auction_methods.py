from flask import Response,abort
from bson.json_util import dumps
import json
from jsonschema import validate
from werkzeug.wrappers import response
from utils import globales
import pymongo

def auction_post(data):
    auction_data = json.loads(data)
    try:
        validate(instance=auction_data,schema=globales.auction_schema)       
        mongo_cli = pymongo.MongoClient(globales.mongodb_uri)
        db = mongo_cli[globales.mongodb_db]
        col = db['auctions']
        if col.count_documents({"code" : auction_data["code"]},limit=1) != 0:
            col.delete_one({"code" : auction_data["code"]})
        op = col.insert_one(auction_data)
        return Response(str(op.inserted_id),200)
    except:
        return Response("BAD FORMAT",401)

def auction_get(codigo):
    mongo_cli = pymongo.MongoClient(globales.mongodb_uri)
    db = mongo_cli[globales.mongodb_db]
    col = db['auctions']
    cursor = col.find({"code" : codigo})
    try:
        doc = cursor.next()
        cursor.close()
        return Response(dumps(doc),200)
    except:
        cursor.close()
        return Response("NOT FOUND",404)

def auction_delete(codigo):
    mongo_cli = pymongo.MongoClient(globales.mongodb_uri)
    db = mongo_cli[globales.mongodb_db]
    col = db['auctions']
    cursor = col.delete_one({"code" : codigo})
    return Response("",200)
