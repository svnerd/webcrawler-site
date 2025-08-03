import os
from openai_generator import synthesize_mp3, get_hiragana_english
import pandas as pd


def _convert_text_conv_list(conv_text:str):

    # Convert to list of (speaker, line) tuples
    conversation = []
    for line in conv_text.strip().splitlines():
        if line.startswith("A:>"):
            conversation.append(("woman", line.replace("A:>", "").strip()))
        elif line.startswith("B:>"):
            conversation.append(("man", line.replace("B:>", "").strip()))
    return conversation


def build_anki_conversation_cards(conv_text:str, api_key, mp3_dir, mp3_base_name):
    """
    Build audio-annotated Anki-style conversation flashcards.
    
    Args:
        conv_text: converstation text delimited by "\n".
        api_key: Your OpenAI API key.
        output_dir: Folder to save MP3 and HTML output.
    """
    conversation = _convert_text_conv_list(conv_text)
    os.makedirs(mp3_dir, exist_ok=True)
    cards = []

    for i, (speaker, line) in enumerate(conversation):
        # Step 1: Generate MP3 filename
        mp3_name = f"{mp3_base_name}_{speaker}_{i}.mp3"
        mp3_path = os.path.join(mp3_dir, mp3_name)

        # Step 2: Synthesize audio
        voice = "shimmer" if speaker == "woman" else "echo"
        synthesize_mp3(line, mp3_path, api_key, voice)

        hiragana, english = get_hiragana_english(line, api_key)
        # Save card
        cards.append({
            "japanese": line,
            "hiragana": hiragana,
            "english": english,
            "audio_path": mp3_name
        })

    # Step 4: Generate HTML
    return pd.DataFrame(cards)
    
