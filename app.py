from flask import Flask, send_from_directory
from const import PAGE_DIR, MP3_DIR, LATEST_DIR
from crawler import run_crawler

import threading

app = Flask(__name__)

@app.route("/robots.txt")
def robots_txt():
    return (
        "User-agent: *\nDisallow: /mp3/\n",
        200,
        {"Content-Type": "text/plain"}
    )

@app.route("/")
def index():
    return send_from_directory(PAGE_DIR, "index.html")

@app.route("/pages/<path:filename>")
def serve_pages(filename):
    return send_from_directory(PAGE_DIR, filename)

@app.route("/mp3/<path:filename>")
def serve_mp3(filename):
    return send_from_directory(MP3_DIR, filename)

@app.route("/api/latest.json")
def serve_latest_json():
    return send_from_directory(LATEST_DIR, "latest.json")

# maybe later will expose latest_en_jp.csv and latest_jp_en.csv for anki.
@app.route("/api/latest.html")
def serve_latest_html():
    return send_from_directory(LATEST_DIR, "latest.html")

# Start crawler in background thread
threading.Thread(target=run_crawler, daemon=True).start()
