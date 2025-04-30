import os
from flask import Flask, render_template
import json

app = Flask(__name__)

# Get absolute path to data.json
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

@app.route("/")
def index():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return render_template("index.html", data=data)

