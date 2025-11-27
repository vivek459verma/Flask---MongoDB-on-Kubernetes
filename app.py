from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Read Mongo settings from environment (with safe defaults for local dev)
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")

if MONGO_USERNAME and MONGO_PASSWORD:
    # Authenticated URI (Kubernetes)
    MONGODB_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/flask_db?authSource=admin"
else:
    # No auth (local dev)
    MONGODB_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

client = MongoClient(MONGODB_URI)
db = client.flask_db
collection = db.data

@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data_route():
    if request.method == "POST":
        # Read JSON from the request body
        data = request.get_json()
        # Insert into MongoDB
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201

    elif request.method == "GET":
        # Fetch all documents except the internal _id field
        docs = list(collection.find({}, {"_id": 0}))
        return jsonify(docs), 200


if __name__ == "__main__":
    # Run the Flask app on port 5000
    app.run(host="0.0.0.0", port=5000)
