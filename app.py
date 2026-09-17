
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, static_folder=".", template_folder=".")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/profile/<username>")
def get_profile(username):
    # Public fetcher helper API response format
    data = {
        "status": "success",
        "username": username,
        "name": username.capitalize(),
        "bio": f"Profile data for @{username}",
        "posts_count": 24,
        "followers_count": 1050,
        "following_count": 300,
        "profile_pic": "https://via.placeholder.com/150",
    }
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
