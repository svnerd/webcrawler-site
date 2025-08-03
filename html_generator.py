
def generate_news_convo_html_mobile_friendly(
        news_text, news_mp3, 
        convo_text, convo_anki_html_path, 
        anki_csv_en_jp, anki_csv_jp_en, anki_en_jp_html, anki_jp_en_html,
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
            <li><a href="/anki/{anki_csv_en_jp}" download>Download English → Japanese (CSV)</a></li>
            <li><a href="/anki/{anki_en_jp_html}" target="_blank"> English → Japanese Anki </a></li>
            <li><a href="/anki/{anki_csv_jp_en}" download>Download Japanese → English (CSV)</a></li>
            <li><a href="/pages/{anki_jp_en_html}" target="_blank"> Japanese → English Anki </a></li>
        </ul>

        <div class="section">
            <h1>💬 会話</h1>
            <p>{convo_html}</p>
            <ul>
                <li><a href="/pages/{convo_anki_html_path}" target="_blank">Conversation Anki Cards</a></li>
            </ul>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {output_path}")

