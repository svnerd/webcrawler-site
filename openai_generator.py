def synthesize_mp3(text, path, api_key):
    """
    Synthesize MP3 using OpenAI API.
    """
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
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
