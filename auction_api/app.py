from flask import Flask,app,jsonify
from api.routes import get_routes

app = Flask(__name__)

get_routes(app)
 
if __name__ == '__main__':
    app.run(debug=True)
