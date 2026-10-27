
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Homepage"

@app.route("/api")
def response():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
