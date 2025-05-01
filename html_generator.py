def generate_news_convo_html(news_text, convo_text, news_mp3, convo_mp3, output_path):
    news_html = news_text.replace("\n", "<br>")
    convo_html = convo_text.replace("\n", "<br>")

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Japanese News & Conversation</title>
    <style>
        body {{
            font-family: "Segoe UI", sans-serif;
            background-color: #f2f2f7;
            color: #222;
            margin: 0;
            padding: 40px;
        }}
        .section {{
            background-color: #fff;
            border-radius: 12px;
            padding: 24px 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            line-height: 1.8;
        }}
        h1 {{
            margin-top: 0;
            font-size: 1.5em;
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
    </style>
</head>
<body>

    <div class="section">
        <h1>📰 ニュース</h1>
        <p>{news_html}</p>
        <a class="audio-link" href="mp3/{news_mp3}" target="_blank">🔊 ニュース音声を聞く (MP3)</a>
    </div>

    <div class="section">
        <h1>💬 会話</h1>
        <p>{convo_html}</p>
        <a class="audio-link" href="mp3/{convo_mp3}" target="_blank">🔊 会話音声を聞く (MP3)</a>
    </div>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML saved to {output_path}")
