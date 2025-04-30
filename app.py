import os
import json
from flask import Flask, render_template

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Create a default file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "title": "Waiting for first crawl...",
            "timestamp": "N/A",
            "message": "No data has been crawled yet."
        }, f)

@app.route("/")
def index():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return render_template("index.html", data=data)


