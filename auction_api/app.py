from flask import Flask,app,jsonify,abort,Response
from api.routes import get_routes
import utils.globales as globales
import os

globales.mongodb_server = os.getenv("MONGO_DB_SERVER") if os.getenv("MONGO_DB_SERVER") else abort(Response("No MONGO DB Server declared", 401))
globales.mongodb_port = os.getenv("MONGO_DB_PORT") if os.getenv("MONGO_DB_PORT") else abort(Response("No MONGO DB PORT declared", 401))
globales.mongodb_user = os.getenv("MONGO_DB_USER") if os.getenv("MONGO_DB_USER") else abort(Response("No MONGO DB username declared", 401))
globales.mongodb_pass = os.getenv("MONGO_DB_PASS") if os.getenv("MONGO_DB_PASS") else abort(Response("No MONGO DB password declared", 401))
globales.mongodb_uri = "mongodb://" + globales.mongodb_user + ":"  +  globales.mongodb_pass + "@" +  globales.mongodb_server + ":" + globales.mongodb_port
print("Starting service")
print("DB URI: mongodb://" + globales.mongodb_user + ":*****@" +  globales.mongodb_server + ":" + globales.mongodb_port)

app = Flask(__name__)
get_routes(app)
if __name__ == '__main__':
    app.run(debug=True)
