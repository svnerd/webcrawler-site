import os
import openai
import csv

def get_hiragana_english(line, api_key):
    # Step 3: Get Hiragana + English via GPT
    annotate_prompt = f"""
    以下の日本語の文章を「ひらがな」＋「英語訳」にしてください。フォーマットはこのようにしてください：
    Hiragana: ...
    English: ...

    日本語: {line}
    """
    try:
        client = openai.OpenAI(api_key=api_key)

        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": annotate_prompt}]
        ).choices[0].message.content

        # Parse result
        hiragana = english = ""
        for l in chat.strip().splitlines():
            if l.lower().startswith("hiragana:"):
                hiragana = l.split(":", 1)[1].strip()
            elif l.lower().startswith("english:"):
                english = l.split(":", 1)[1].strip()
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe: {e}")
    return hiragana, english

def synthesize_mp3(text, path, api_key, voice="echo"):
    """
    Synthesize MP3 using OpenAI API.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        with open(path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        raise RuntimeError(f"Failed to synthesize MP3: {e}")
    

def construct_conversation(article_text, api_key):
    # STEP 1: Generate conversation
    conversation_prompt = f"""
    次のニュースを読んだ人たちが、自然に交わす短い会話を日本語で書いてください。
    友達や家族、同僚などの日常的な会話スタイルでお願いします。
    Please mark roles with A:> , B:>  

    ニュース:
    {article_text}
    """
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": conversation_prompt}
        ]
    )
    return response.choices[0].message.content


def generate_anki_from_text(
        input_text, openai_api_key, 
        jp_en_csv, en_jp_csv
):
    client = openai.OpenAI(api_key=openai_api_key)

    prompt = f"""
あなたは日本語教師です。次の文章からJLPT N3レベル以上（N3、N2、N1）の語彙を含む短い自然な日本語フレーズを抽出してください。
各フレーズには、1つ以上のN3以上の語彙を含めてください。

さらに、各フレーズについて以下の情報を出力してください：
1. フレーズ（元の日本語）
2. フレーズ（全ての漢字にふりがなを付けたもの）
3. 英語訳

出力形式：
フレーズ: <phrase>
ふりがな: <phrase with furigana>
英語訳: <english translation>

5セット出力してください。説明文や追加情報は不要です。
文章:
{input_text}
"""

    chat_completion = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4" if preferred
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    output = chat_completion.choices[0].message.content

    # Parse response
    cards = []
    for block in output.strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) == 3:
            phrase = lines[0].replace("フレーズ:", "").strip()
            furigana = lines[1].replace("ふりがな:", "").strip()
            english = lines[2].replace("英語訳:", "").strip()
            cards.append((phrase, furigana, english))

    # Write Japanese → English file
    with open(jp_en_csv, "w", newline='', encoding='utf-8') as csvfile_jp_en:
        writer_jp_en = csv.writer(csvfile_jp_en)
        writer_jp_en.writerow(["Front", "Back"])
        
        for phrase, furigana, english in cards:
            back = f"{furigana}<br>{english}"
            writer_jp_en.writerow([phrase, back])

    # Write English → Japanese file
    with open(en_jp_csv, "w", newline='', encoding='utf-8') as csvfile_en_jp:
        writer_en_jp = csv.writer(csvfile_en_jp)
        writer_en_jp.writerow(["Front", "Back"])
        
        for phrase, furigana, english in cards:
            writer_en_jp.writerow([english, f"{phrase}<br>{furigana}"])

    print(f"Anki cards saved to {jp_en_csv} and {en_jp_csv}")
