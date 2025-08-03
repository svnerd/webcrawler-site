
import pandas as pd

def write_anki_conversation_html(conversation_df: pd.DataFrame, target_html_path: str):
    with open(target_html_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      font-family: sans-serif;
      margin: 0;
      padding: 0;
      background: #f0f0f0;
    }}
    h2 {{
      text-align: center;
      margin-top: 20px;
      font-size: 22px;
    }}
    .container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px;
    }}
    .card {{
      width: 100%;
      max-width: 600px;
      background: white;
      margin: 15px 0;
      padding: 16px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      box-sizing: border-box;
    }}
    .front {{
      font-size: 16px;
      color: darkgreen;
      margin-bottom: 10px;
      word-wrap: break-word;
    }}
    .flip-button {{
      display: block;
      font-size: 14px;
      padding: 8px 14px;
      margin: 10px 0;
      border: none;
      background-color: #1976d2;
      color: white;
      border-radius: 6px;
      cursor: pointer;
      width: 100px;
    }}
    .back {{
      display: none;
      margin-top: 10px;
    }}
    .japanese {{
      font-size: 18px;
      margin-bottom: 8px;
    }}
    .hiragana {{
      font-size: 14px;
      color: gray;
      margin-bottom: 6px;
    }}
    audio {{
      width: 100%;
      margin-top: 8px;
    }}
    @media (max-width: 480px) {{
      .card {{
        padding: 12px;
        border-radius: 10px;
      }}
      .japanese {{
        font-size: 16px;
      }}
    }}
  </style>
  <script>
    function toggleCard(id) {{
      const back = document.getElementById("back-" + id);
      const btn = document.getElementById("flip-btn-" + id);
      if (back.style.display === "block") {{
        back.style.display = "none";
        btn.innerText = "Flip";
      }} else {{
        back.style.display = "block";
        btn.innerText = "Hide";
      }}
    }}
  </script>
</head>
<body>
<h2>Japanese Conversation Flashcards</h2>
<div class="container">
''')

        for i, row in conversation_df.iterrows():
            f.write(f'''
  <div class="card" id="card-{i}">
    <div class="front">{row['english']}</div>
    <button class="flip-button" id="flip-btn-{i}" onclick="toggleCard('{i}')">Flip</button>
    <div class="back" id="back-{i}">
      <div class="japanese">{row['japanese']}</div>
      <div class="hiragana">{row['hiragana']}</div>
      <audio controls src="/mp3/{row['audio_path']}"></audio>
    </div>
  </div>
''')

        f.write('''
</div>
</body>
</html>
''')

    print(f"✅ Mobile-friendly flip-card HTML saved to: {target_html_path}")


import pandas as pd

def write_anki_vocab_html(vocab_csv: str, target_html_path: str):
    conversation_df = pd.read_csv(vocab_csv)
    with open(target_html_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Japanese Conversation Flashcards</title>
  <style>
    body {{
      font-family: sans-serif;
      margin: 0;
      padding: 0;
      background: #f0f0f0;
    }}
    h2 {{
      text-align: center;
      margin-top: 20px;
      font-size: 22px;
    }}
    .container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px;
    }}
    .card {{
      width: 100%;
      max-width: 600px;
      background: white;
      margin: 15px 0;
      padding: 16px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      box-sizing: border-box;
    }}
    .front {{
      font-size: 16px;
      color: darkgreen;
      margin-bottom: 10px;
      word-wrap: break-word;
    }}
    .flip-button {{
      display: block;
      font-size: 14px;
      padding: 8px 14px;
      margin: 10px 0;
      border: none;
      background-color: #1976d2;
      color: white;
      border-radius: 6px;
      cursor: pointer;
      width: 100px;
    }}
    .back {{
      display: none;
      margin-top: 10px;
    }}
    .japanese {{
      font-size: 18px;
      margin-bottom: 8px;
    }}
    @media (max-width: 480px) {{
      .card {{
        padding: 12px;
        border-radius: 10px;
      }}
      .japanese {{
        font-size: 16px;
      }}
    }}
  </style>
  <script>
    function toggleCard(id) {{
      const back = document.getElementById("back-" + id);
      const btn = document.getElementById("flip-btn-" + id);
      if (back.style.display === "block") {{
        back.style.display = "none";
        btn.innerText = "Flip";
      }} else {{
        back.style.display = "block";
        btn.innerText = "Hide";
      }}
    }}
  </script>
</head>
<body>
<h2>Japanese Conversation Flashcards</h2>
<div class="container">
''')

        for i, row in conversation_df.iterrows():
            front = row['Front']
            back = row['Back']
            f.write(f'''
  <div class="card" id="card-{i}">
    <div class="front">{front}</div>
    <button class="flip-button" id="flip-btn-{i}" onclick="toggleCard('{i}')">Flip</button>
    <div class="back" id="back-{i}">
      <div class="japanese">{back}</div>
    </div>
  </div>
''')

        f.write('</div></body></html>')

    print(f"✅ HTML saved to: {target_html_path}")