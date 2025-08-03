from jinja2 import Environment, FileSystemLoader
from const import PAGE_DIR
import os
from html_generator import generate_news_convo_html_mobile_friendly
from const import PAGE_DIR, LATEST_DIR
import json
import shutil


def generate_html_from_json(json_data):
    base_name = json_data["base_name"]
    html_base_name = f"{base_name}.html"
    html_path = os.path.join(PAGE_DIR, html_base_name)
    text = json_data["text"]
    convo_text = json_data["convo_text"]
    news_link = json_data["url"]

    # file names. 
    news_mp3_path = f"{base_name}_news.mp3"
    en_jp_csv = f"{base_name}_en_jp.csv"
    jp_en_csv = f"{base_name}_jp_en.csv"
    en_jp_html = f"{base_name}_vocab_en_jp.html"
    jp_en_html = f"{base_name}_vocab_jp_en.html"

    # Save HTML
    generate_news_convo_html_mobile_friendly(
        # text related
        text, news_mp3_path,
        # conversation related
        convo_text, json_data["conv_anki_html_path"],
        # anki related  
        en_jp_csv, jp_en_csv,
        en_jp_html, jp_en_html, 
        output_path=html_path, top_link=news_link)
    return html_base_name

def generate_latest_json(json_data_list):
    """
    Write the latest news data to a JSON file.
    """
    if not json_data_list:
        print("❌ No data available to generate latest.json")
        return

    latest_json_path = os.path.join(LATEST_DIR, "latest.json")
    os.makedirs(LATEST_DIR, exist_ok=True)  # Ensure the directory exists

    try:
        with open(latest_json_path, "w", encoding="utf-8") as f:
            json.dump(json_data_list[0], f, ensure_ascii=False, indent=2)
        print(f"✅ Latest news saved to {latest_json_path}")
    except Exception as e:
        print(f"❌ Failed to write latest.json: {e}")


def generate_to_public(json_data_list):
    # generate the main site index.html
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.j2")
    html_files = []
    for json_data in json_data_list:
        html_files.append(generate_html_from_json(json_data))
    rendered = template.render(news_pages=html_files)
    with open(os.path.join(PAGE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)
    # generate api related files. e.g. latest.json, latest.html
    generate_latest_json(json_data_list)
    if len(html_files) > 0:
        shutil.copy(
            os.path.join(PAGE_DIR, html_files[0]),
            os.path.join(LATEST_DIR, "latest.html"))
