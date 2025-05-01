from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("/mnt/data", "index.html")

@app.route("/pages/<path:filename>")
def serve_pages(filename):
    return send_from_directory("/mnt/data/pages", filename)