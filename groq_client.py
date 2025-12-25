import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"


def translate_text(source_lang, target_lang, text):
    system_prompt = f"""
You are a professional translation engine.

Translate text from {source_lang} to {target_lang}.
Rules:
Output ONLY the translated text
- DO NOT add explanations
- DO NOT add examples
- DO NOT ask questions
- DO NOT add greetings
- DO NOT add notes
- Preserve punctuation and formatting
- Keep line breaks exactly as given
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        max_tokens=2048
    )

    return response.choices[0].message.content.strip()
