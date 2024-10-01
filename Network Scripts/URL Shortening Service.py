import hashlib
import os
import string
import secrets
from urllib.parse import urlparse

from flask import Flask, redirect, request, jsonify
from pymongo import MongoClient
from validators import url as validate_url

app = Flask(__name__)

# Connect to the database
try:
    client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"))
    db = client["url_shortener"]
    urls = db["urls"]
except Exception as e:
    print("Error connecting to the database:", e)
    exit(1)

def generate_short_url():
    length = 6
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(secrets.choice(characters) for _ in range(length))
        if not urls.find_one({"short_url": short_url}):
            return short_url

def hash_url(original_url):
    hash_obj = hashlib.sha256(original_url.encode())
    return hash_obj.hexdigest()[:10]

@app.route("/shorten", methods=["POST"])
def shorten():
    # Get the original URL from the request
    original_url = request.form.get("url")

    # Validate the URL
    if not validate_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Check if the URL already exists in the database
    hashed_url = hash_url(original_url)
    existing_url = urls.find_one({"hashed_url": hashed_url})
    if existing_url:
        return jsonify({"short_url": f"http://localhost:5000/{existing_url['short_url']}"})

    # Generate a unique identifier for the URL
    short_url = generate_short_url()

    # Store the original and shortened URLs in the database
    urls.insert_one({"original_url": original_url, "short_url": short_url, "hashed_url": hashed_url})

    # Return the shortened URL
    return jsonify({"short_url": f"http://localhost:5000/{short_url}"})

@app.route("/<short_url>")
def redirect_url(short_url):
    # Look up the original URL in the database using the shortened URL
    url_data = urls.find_one({"short_url": short_url})
    if url_data:
        # Redirect to the original URL
        return redirect(url_data["original_url"])
    else:
        # Short URL not found
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run()