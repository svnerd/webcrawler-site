import json
from datetime import datetime

def fetch_data():
    return {
        "title": "Web Crawling Example",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "This data was 'crawled' and saved automatically."
    }

if __name__ == "__main__":
    data = fetch_data()
    with open("data.json", "w") as f:
        json.dump(data, f)