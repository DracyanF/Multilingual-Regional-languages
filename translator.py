from groq_client import translate_text
from chunking import chunk_text
from utils import LANG_MAP


def translate_blocks(blocks, source_lang, target_lang):
    translated = []

    for text in blocks:
        if not text.strip():
            translated.append(text)
            continue

        chunks = chunk_text(text)
        translated_chunks = []

        for chunk in chunks:
            translated_chunks.append(
                translate_text(source_lang, target_lang, chunk)
            )

        translated.append("".join(translated_chunks))

    return translated
