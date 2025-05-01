import os
import json
from datetime import datetime

DATA_FILE = os.path.join("/debug/webcrawler", 'data.json')

def fetch_data():
    return {
        "title": "Web Crawling Example",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "This data was 'crawled' and saved automatically."
    }

if __name__ == "__main__":
    os.makedirs("/debug/webcrawler", exist_ok=True)
    data = fetch_data()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

