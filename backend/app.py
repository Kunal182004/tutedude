
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from pathlib import Path
import os

load_dotenv()

app = Flask(__name__)

uri = os.getenv("MONGO_URL")

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client["test"]
collection = db["users"]


@app.route("/")
def home():
    return render_template("index.html", error=None)


@app.route("/login", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return render_template(
            "index.html",
            error="Username and password are required."
        ), 400

    try:
        # Check that MongoDB is reachable.
        client.admin.command("ping")

        user = {
            "username": username,
            "password": generate_password_hash(password)
        }

        collection.insert_one(user)

        return redirect(url_for("success"))

    except Exception:
        app.logger.exception("Registration failed")

        return render_template(
            "index.html",
            error="Unable to submit data. Please try again."
        ), 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
