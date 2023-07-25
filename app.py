from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

username = process.env.MONGO_USERNAME
password = process.env.MONGO_PASSWORD

# MongoDB connection setup
uri = f"mongodb+srv://{username}:{password}@cluster0.faieny2.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(MONGO_URI)
client = MongoClient(uri)


db = client["curl_messages"]
collection = db["messages"]

# Function to insert a new message into the database
def insert_message(curl_message):
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    message_data = {"timestamp": timestamp, "curl_message": curl_message}
    collection.insert_one(message_data)

# Function to retrieve all messages from the database
def get_messages():
    messages = collection.find().sort("timestamp", -1)
    message_list = [
        {"timestamp": msg["timestamp"], "curl_message": msg["curl_message"]}
        for msg in messages
    ]
    return message_list

@app.route("/", methods=["POST"])
def store_message():
    data = request.get_json("curl_message")
    curl_message = data.get("curl_message")
    if curl_message is not None and curl_message.strip():
        insert_message(curl_message)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure", "message": "Empty cURL message"})


@app.route("/get_messages", methods=["GET"])
def fetch_messages():
    messages = get_messages()
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True)
