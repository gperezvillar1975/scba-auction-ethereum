import pymongo
from werkzeug.wrappers.response import Response 
import utils.globales as globales
from bson.json_util import dumps

def get_requests_by_status(status):
    if status not in ["0","1"]:
        return Response("Invalid Status",400)

    mongo_cli = pymongo.MongoClient(globales.mongodb_uri)
    db = mongo_cli[globales.mongodb_db]
    col = db['bidders']
    cur = col.find({"status" : int(status)})
    result = dumps(cur)
    cur.close()
    return Response(result,200)
def delete_pending_requests(id_number):
    pass
def approve_pending_requests(id_number):
    pass
