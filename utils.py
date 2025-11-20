import json
import re

def extract_claim_json(text: str):
    if not text or not isinstance(text, str):
        return None

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    json_pattern = re.compile(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", re.DOTALL)
    match = json_pattern.search(text)

    if not match:
        return None

    json_str = match.group(0).strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        cleaned = re.sub(r"[\x00-\x1F]+", "", json_str)
        try:
            return json.loads(cleaned)
        except:
            return None
