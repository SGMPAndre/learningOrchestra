from flask import jsonify, request, Flask
import os
from constants import Constants
import json

app = Flask(__name__)

@app.route(Constants.MICROSERVICE_URI_PATH, methods=["POST"])
def create_file():
    pass

if __name__ == "__main__":
    app.run(host=os.environ[Constants.MICROSERVICE_IP],
            port=int(os.environ[Constants.MICROSERVICE_PORT]))
