from jinja2 import Environment, FileSystemLoader
from const import PAGE_DIR
import os

def generate_index():
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.j2")
    files = sorted(os.listdir(PAGE_DIR), reverse=True)
    html_files = [f for f in files if f.endswith(".html") and not f.startswith("index")]
    rendered = template.render(news_pages=html_files)
    with open(os.path.join(PAGE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)

