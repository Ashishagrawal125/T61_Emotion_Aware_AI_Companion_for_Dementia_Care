from langdetect import detect
from deep_translator import GoogleTranslator


def _safe_lang(code: str) -> str:
    if not code:
        return "en"
    code = code.lower()
    if "-" in code:
        code = code.split("-")[0]
    return code


def detect_and_translate(text: str) -> str:
    if not text or not text.strip():
        return ""
    detected_lang = _safe_lang(detect(text))
    if detected_lang == "en":
        return text
    return GoogleTranslator(source=detected_lang, target="en").translate(text)


def change_to_target(text: str, target_lang: str):
    if not text or not text.strip():
        return "", "en"
    detected_lang = _safe_lang(detect(text))
    target_lang = _safe_lang(target_lang)
    if detected_lang == target_lang:
        return text, detected_lang
    translated = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
    return translated, detected_lang
