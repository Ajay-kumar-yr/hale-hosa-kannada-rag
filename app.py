from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os
import json
import time
import re


# ============================================================
# 1. LOAD API KEY FROM .env
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )


# ============================================================
# 2. FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# 3. GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# 4. HELPERS
# ============================================================

def contains_english(text):
    return bool(re.search(r"[A-Za-z]", text))


def contains_kannada(text):
    return bool(re.search(r"[\u0C80-\u0CFF]", text))


# ============================================================
# 5. SYSTEM INSTRUCTION (rules + few-shot examples)
# ============================================================
#
# NOTE: Replace/expand the example pairs below with real,
# verified Hale -> Hosa Kannada translations. The quality of
# these examples matters more than almost anything else here —
# add as many as you can (10-20+ is ideal) covering different
# grammatical forms (verbs, nouns, sentence endings, etc.).

SYSTEM_INSTRUCTION = """You are an expert linguist specializing exclusively in translating Hale Kannada (Old / Medieval Kannada) into Hosa Kannada (Modern Kannada).

Rules:
1. Output ONLY the Hosa Kannada translation. Nothing else.
2. Never include English words, English letters, or transliteration.
3. Never explain, define, or give the English meaning.
4. Never add labels like "Translation:", "Hosa Kannada:", "Answer:", etc.
5. Never give multiple alternative answers, bullet points, or numbering.
6. If the input is ambiguous or already looks like Hosa Kannada, still return your best Hosa Kannada rendering — never refuse, never respond in English.
7. Preserve the original meaning, tense, and tone (formal/informal, poetic/plain) as closely as possible.
8. Use Kannada script only, in the "hosa_kannada_translation" field.

Examples:
Hale Kannada: ಮಾಡಿದಂ
Hosa Kannada: ಮಾಡಿದನು

Hale Kannada: ಪೇೞ್ದಂ
Hosa Kannada: ಹೇಳಿದನು

Hale Kannada: ಬಂದಪ್ಪುದು
Hosa Kannada: ಬರುತ್ತದೆ

Hale Kannada: ಎಂದುಂ
Hosa Kannada: ಎಂದೂ

Hale Kannada: ನೃಪತುಂಗದೇವಂ
Hosa Kannada: ನೃಪತುಂಗದೇವನು

Always respond with a single JSON object in this exact shape:
{"hosa_kannada_translation": "<only the Kannada translation here>"}
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "hosa_kannada_translation": {"type": "string"}
    },
    "required": ["hosa_kannada_translation"]
}


# ============================================================
# 6. HALE KANNADA -> HOSA KANNADA
# ============================================================

def translate_hale_to_hosa(hale_text):

    # Verify these model names against Google's current model
    # list before relying on them — names change over time.
    models = [
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite"
    ]

    last_error = None

    for model in models:

        for attempt in range(2):

            try:

                print(f"Trying model: {model} (attempt {attempt + 1})")

                response = client.models.generate_content(
                    model=model,
                    contents=hale_text,
                    config={
                        "system_instruction": SYSTEM_INSTRUCTION,
                        "temperature": 0.1,
                        "response_mime_type": "application/json",
                        "response_schema": RESPONSE_SCHEMA
                    }
                )

                if not response.text:
                    raise Exception("Gemini returned an empty response.")

                print(f"Gemini raw response: {response.text}")

                data = json.loads(response.text)
                translation = data.get("hosa_kannada_translation", "").strip()

                print(f"Parsed translation: {translation}")

                # Accept only if it looks like real Kannada output
                if translation and contains_kannada(translation) and not contains_english(translation):
                    return translation

                print("Response was empty, non-Kannada, or contained English. Retrying...")

            except json.JSONDecodeError as e:

                last_error = e
                print(f"JSON parse error: {e}")
                continue

            except Exception as e:

                last_error = e
                print(f"Gemini error: {e}")

                if "503" in str(e):
                    print("Gemini is temporarily unavailable.")
                    if attempt == 0:
                        print("Retrying after 3 seconds...")
                        time.sleep(3)
                    continue

                # Other errors: try next attempt/model rather than
                # aborting immediately
                continue

    raise Exception(
        "Gemini is temporarily unavailable. Please try again later."
        + (f" (last error: {last_error})" if last_error else "")
    )


# ============================================================
# 7. HOME PAGE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    hale_text = ""
    translation = ""
    error = ""

    if request.method == "POST":

        hale_text = request.form.get("hale_text", "").strip()

        if not hale_text:
            error = (
                "ದಯವಿಟ್ಟು ಹಳೆಗನ್ನಡ ಪದ ಅಥವಾ "
                "ವಾಕ್ಯವನ್ನು ನಮೂದಿಸಿ."
            )
        else:
            try:
                translation = translate_hale_to_hosa(hale_text)
            except Exception as e:
                print(f"Translation error: {e}")
                error = (
                    "ಅನುವಾದ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. "
                    "ದಯವಿಟ್ಟು ಕೆಲವು ಸೆಕೆಂಡುಗಳ ನಂತರ "
                    "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
                )

    return render_template(
        "index.html",
        hale_text=hale_text,
        translation=translation,
        error=error
    )


# ============================================================
# 8. START FLASK
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("     HALE KANNADA -> HOSA KANNADA")
    print("=" * 55)
    print()
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )