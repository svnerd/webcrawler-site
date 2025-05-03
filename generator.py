from jinja2 import Environment, FileSystemLoader
from const import PAGE_DIR
import os
from html_generator import generate_news_convo_html


def generate_html_from_json(json_data):
    base_name = json_data["base_name"]
    html_path = os.path.join(PAGE_DIR, f"{base_name}.html")
    text = json_data["text"]
    convo_text = json_data["convo_text"]
    # Save HTML
    generate_news_convo_html(
        text, convo_text, 
        f"{base_name}_news.mp3", f"{base_name}_conv.mp3",
        html_path)
    return html_path

def generate_index(json_data_list):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.j2")
    html_files = []
    for json_data in json_data_list:
        html_files.append(generate_html_from_json(json_data))
    rendered = template.render(news_pages=html_files)
    with open(os.path.join(PAGE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)


from const import PAGE_DIR, LATEST_JSON_DIR  # Import LATEST_JSON_DIR
import json

def generate_latest_json(json_data_list):
    """
    Write the latest news data to a JSON file.
    """
    if not json_data_list:
        print("❌ No data available to generate latest.json")
        return

    latest_json_path = os.path.join(LATEST_JSON_DIR, "latest.json")
    os.makedirs(LATEST_JSON_DIR, exist_ok=True)  # Ensure the directory exists

    try:
        with open(latest_json_path, "w", encoding="utf-8") as f:
            json.dump(json_data_list[0], f, ensure_ascii=False, indent=2)
        print(f"✅ Latest news saved to {latest_json_path}")
    except Exception as e:
        print(f"❌ Failed to write latest.json: {e}")
