from google import genai
import os
import json
client = genai.Client(api_key="GET_API_KEY")



MODEL = "gemini-3.1-flash-lite"


def score_metric(value, low, high, hard_low, hard_high):
    """Returns 0-100. 100 = dead center of normal range, decaying toward hard limits."""
    mid = (low + high) / 2
    half_range = (high - low) / 2

    if low <= value <= high:
        deviation = abs(value - mid) / half_range
        return round(100 - (deviation * 20))

    if value < low:
        span = low - hard_low
        over = low - value
    else:
        span = hard_high - high
        over = value - high

    if span <= 0:
        return 0

    penalty = min(over / span, 1) * 80
    return round(max(0, 80 - penalty))


def calculate_health_score(data):
    scores = {
        "blood_sugar": score_metric(data["blood_sugar"], low=70, high=100, hard_low=40, hard_high=250),
        "cholesterol": score_metric(data["cholesterol"], low=125, high=200, hard_low=80, hard_high=320),
        "hemoglobin":  score_metric(data["hemoglobin"], low=12, high=16.5, hard_low=6, hard_high=20),
    }
    weights = {"blood_sugar": 0.4, "cholesterol": 0.35, "hemoglobin": 0.25}
    total = sum(scores[k] * weights[k] for k in scores)
    return round(total), scores


def risk_from_score(score):
    if score >= 75:
        return "Low"
    if score >= 50:
        return "Moderate"
    return "High"


def clean_json_text(raw):
    """Gemini occasionally wraps output in backticks/whitespace despite instructions."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()


def predict_health(data):
    health_score, breakdown = calculate_health_score(data)
    risk = risk_from_score(health_score)

    prompt = f"""
You are a health expert.

Patient values:
Blood Sugar: {data['blood_sugar']} mg/dL
Cholesterol: {data['cholesterol']} mg/dL
Hemoglobin: {data['hemoglobin']} g/dL

A risk level of "{risk}" has already been determined from standard clinical
reference ranges. Do not override it — write advice consistent with it.

Return ONLY valid JSON in this format:

{{
  "good_news":[
    "...",
    "..."
  ],
  "medical_advice":[
    "...",
    "..."
  ],
  "lifestyle":[
    "...",
    "..."
  ],
  "hospital":{{
      "name":"",
      "city":""
  }}
}}

Do not include "risk" or "health_score" fields — they are added separately.
Do not use markdown.
Do not use ```json.
Return only JSON.
"""
    response = client.models.generate_content(model=MODEL, contents=prompt)

    try:
        ai_result = json.loads(clean_json_text(response.text))
    except json.JSONDecodeError:
        # graceful fallback so a malformed response doesn't 500 the request
        ai_result = {
            "good_news": [],
            "medical_advice": ["AI response could not be parsed. Please try again."],
            "lifestyle": [],
            "hospital": {"name": "", "city": ""},
        }

    ai_result["risk"] = risk
    ai_result["health_score"] = health_score
    ai_result["score_breakdown"] = breakdown  # optional: useful for debugging/audit trail

    return ai_result