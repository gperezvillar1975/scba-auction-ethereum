import json
from eth_account import Account
from jsonschema import validate
from werkzeug.wrappers.response import Response 
from utils import globales
import secrets
import string
import hashlib
import pymongo

def bidder_request(data):
    bidder_data = json.loads(data)
    try:
        validate(instance=bidder_data,schema=globales.bidder_schema)           
        # Generates temp password
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(12)) 
        print("One time Password: " + password)
        pass_hash = hashlib.sha256(str.encode(password))
        bidder_data["pass_sha256"] = pass_hash.hexdigest()
        # Create bidder eth wallet
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        print("Wallet address: " + acct.address)
        bidder_data["wallet_address"] = acct.address
        bidder_data["wallet_pk"] = private_key
        bidder_data["status"] = 0
        # Save data to DB
        mongo_cli = pymongo.MongoClient(globales.mongodb_uri)
        db = mongo_cli[globales.mongodb_db]
        col = db['bidders']
        if col.count_documents({"id_number" : bidder_data["id_number"]},limit=1) != 0:
            return Response("Duplicate request !!!",400)
        op = col.insert_one(bidder_data)        
        return Response("OK",200)
    except:
        return Response("Bad Format",400)