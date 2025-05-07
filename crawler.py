import os
import time
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from const import (
    BASE_URL, NEWS_LIST_URL, JSON_DIR, MP3_DIR, 
    PAGE_DIR, MAX_ARTICLES, ANKI_DIR, LATEST_DIR
)
from generator import generate_to_public
from openai_generator import synthesize_mp3, construct_conversation, generate_anki_from_text


def setup_directories():
    """
    Ensure necessary directories exist.
    """
    for directory in [JSON_DIR, MP3_DIR, PAGE_DIR, LATEST_DIR, ANKI_DIR]:
        os.makedirs(directory, exist_ok=True)

def extract_article_text(news_id):
    url = f"{BASE_URL}/{news_id}/{news_id}.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Attempt to find the main article content
    article_body = soup.find('div', id='js-article-body')
    if not article_body:
        print("Article body not found.")
        return None

    # Extract text from paragraphs within the article body
    paragraphs = article_body.find_all('p')
    article_text = '\n'.join([para.get_text(strip=True) for para in paragraphs])
    return article_text


def process_news_item(item, date, api_key) -> dict:
    """
    Process a single news item.
    """
    news_id = item["news_id"]
    title = item["title"]
    date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
    base_name = f"{date_str}_{news_id}"

    json_path = os.path.join(JSON_DIR, f"{base_name}.json")
    news_mp3_path = os.path.join(MP3_DIR, f"{base_name}_news.mp3")
    jp_en_csv = os.path.join(ANKI_DIR, f"{base_name}_jp_en.csv")
    en_jp_csv = os.path.join(ANKI_DIR, f"{base_name}_en_jp.csv")

    # Skip if all files already exist
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        print(f"⚠️ Skipping {base_name}, already exists.")
        return json_data
        
    try:
        text = extract_article_text(news_id)
        convo_text = construct_conversation(text, api_key)
        synthesize_mp3(text, news_mp3_path, api_key)

        generate_anki_from_text(text, api_key, )
        article_data = {
            'base_name': base_name,
            "title": title,
            "id": news_id,
            "date": date,
            "url": f"{BASE_URL}/{news_id}/{news_id}.html",
            "text": text,
            "convo_text": convo_text,
            'jp_en_csv': jp_en_csv,
            'en_jp_csv': en_jp_csv,
        }
        
        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        # Generate MP3
        print(f"✅ Processed: {base_name}")
        return article_data
    except Exception as e:
        print(f"❌ Error processing {news_id}: {e}")
        return None

def crawl(api_key):
    """
    Main crawling function.
    """
    try:
        res = requests.get(NEWS_LIST_URL)
        res.raise_for_status()
        res.encoding = "utf-8"
        all_news = res.json()[0]
    except requests.RequestException as e:
        print(f"Failed to fetch news list: {e}")
        return

    json_data_list = []
    for date, items in sorted(all_news.items(), reverse=True):
        for item in items:
            json_item = process_news_item(item, date, api_key)
            if json_item is not None:
                json_data_list.append(json_item)
            else:
                print(f"❌ Failed to process {item}")
            if len(json_data_list) >= MAX_ARTICLES:
                break
        if len(json_data_list) >= MAX_ARTICLES:
            break
    generate_to_public(json_data_list)
    print("✅ Finished generating index and latest.json")

def run_crawler():
    """
    Run the crawler in a loop.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY")
    setup_directories()
    while True:
        print("🕷 Starting daily crawl...")
        crawl(api_key)
        print("✅ Finished crawling. Sleeping for 24 hours...")
        time.sleep(60 * 60 * 24)
        # 24 hours = 86400 seconds
        


if __name__ == "__main__":
    run_crawler()