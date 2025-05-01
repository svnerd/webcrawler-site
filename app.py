from flask import Flask, send_from_directory
from const import PAGE_DIR, MP3_DIR
from crawler import run_crawler

import threading

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(PAGE_DIR, "index.html")

@app.route("/pages/<path:filename>")
def serve_pages(filename):
    return send_from_directory(PAGE_DIR, filename)

@app.route("/mp3/<path:filename>")
def serve_mp3(filename):
    return send_from_directory(MP3_DIR, filename)


# Start crawler in background thread
threading.Thread(target=run_crawler, daemon=True).start()
