import pandas as pd

def generate_flashcards_html(df: pd.DataFrame, output_path: str):
    """
    Generate a mobile-friendly HTML flashcard viewer from a DataFrame with 'Front' and 'Back' columns.

    Args:
        df (pd.DataFrame): A DataFrame with 'Front' and 'Back' columns.
        output_path (str): The path to write the generated HTML file to.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Anki-style Flashcards (EN → JP)</title>
  <style>
    body {{
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
      background: #f8f8f8;
    }}
    .card-wrapper {{
      display: flex;
      flex-direction: row;
      align-items: stretch;
      margin: 15px;
      width: 100%;
      max-width: 600px;
    }}
    .toggle-button {{
      writing-mode: vertical-rl;
      transform: rotate(180deg);
      padding: 10px 5px;
      font-size: 12px;
      cursor: pointer;
      width: 30px;
      border: 1px solid #ccc;
      border-radius: 5px 0 0 5px;
      background-color: #eee;
      flex-shrink: 0;
    }}
    .card {{
      flex-grow: 1;
      padding: 15px 20px;
      border: 1px solid #ccc;
      border-radius: 0 10px 10px 0;
      background: white;
      text-align: left;
      box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
      overflow-y: auto;
      min-height: 120px;
    }}
    .front {{
      font-size: 16px;
    }}
    .back {{
      display: none;
      margin-top: 10px;
      color: darkgreen;
    }}
    @media (max-width: 480px) {{
      .card-wrapper {{
        flex-direction: column;
        max-width: 100%;
      }}
      .toggle-button {{
        writing-mode: horizontal-tb;
        transform: none;
        width: 100%;
        border-radius: 5px 5px 0 0;
      }}
      .card {{
        border-radius: 0 0 10px 10px;
      }}
    }}
  </style>
  <script>
    function toggleAnswer(id) {{
      const back = document.getElementById("back-" + id);
      if (back.style.display === "block") {{
        back.style.display = "none";
      }} else {{
        back.style.display = "block";
      }}
    }}
  </script>
</head>
<body>
<h2>English → Japanese Flashcards</h2>
<div id="cards-container">
''')

        for i, row in df.iterrows():
            front = row['Front']
            back = row['Back']
            f.write(f'''
  <div class="card-wrapper">
    <button class="toggle-button" onclick="toggleAnswer('{i}')">Show<br>Hide</button>
    <div class="card" id="card-{i}">
      <div class="front">{front}</div>
      <div class="back" id="back-{i}">{back}</div>
    </div>
  </div>
''')

        f.write('''
</div>
</body>
</html>
''')

    print(f"✅ Flashcards saved to {output_path}")


def generate_news_convo_html_mobile_friendly(
        news_text, convo_text, news_mp3, 
        anki_csv_jp_en, anki_csv_en_jp,
        output_path, top_link=None):
    news_html = news_text.replace("\n", "<br>")
    convo_html = convo_text.replace("\n", "<br>")

    top_link_html = f'<a href="{top_link}" class="top-link">🔗 NHK Easy News Original Link </a>' if top_link else ""

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8M1B4RFFRD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-8M1B4RFFRD');
</script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Japanese News & Conversation</title>
    <style>
        body {{
            font-family: "Segoe UI", sans-serif;
            background-color: #f2f2f7;
            color: #222;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .section {{
            background-color: #fff;
            border-radius: 12px;
            padding: 16px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 24px;
        }}
        h1 {{
            margin-top: 0;
            font-size: 1.4em;
            color: #333;
        }}
        a.audio-link {{
            display: inline-block;
            margin-top: 12px;
            color: #007acc;
            text-decoration: none;
        }}
        a.audio-link:hover {{
            text-decoration: underline;
        }}
        .top-link {{
            display: block;
            margin-bottom: 20px;
            color: #007acc;
            text-decoration: none;
            font-size: 0.9em;
        }}
        .top-link:hover {{
            text-decoration: underline;
        }}
        audio {{
            width: 100%;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {top_link_html}

        <div class="section">
            <h1>📰 ニュース</h1>
            <p>{news_html}</p>
            <span>🔊 ニュース音声を聞く</span>
            <audio controls>
                <source src="/mp3/{news_mp3}" type="audio/mpeg">
                <a class="audio-link" href="/mp3/{news_mp3}" target="_blank">🔊 ニュース音声を聞く (MP3)</a>
            </audio>
        </div>

        <div class="section">
        <h1>Download your Anki CSV files:</h1>
        <ul>
            <li><a href="/anki/{anki_csv_jp_en}" download>Download Japanese → English (CSV)</a></li>
            <li><a href="/anki/{anki_csv_en_jp}" download>Download English → Japanese (CSV)</a></li>
        </ul>

        <div class="section">
            <h1>💬 会話</h1>
            <p>{convo_html}</p>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {output_path}")

