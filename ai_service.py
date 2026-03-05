import os
import json
import httpx
from typing import Any, Dict

DO_API_URL = os.getenv(
    "DO_SERVERLESS_INFERENCE_API_URL",
    "https://api.digitalocean.com/v2/gen-ai/chat/completions"
)
DO_API_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY", "")
MODEL = os.getenv("DO_INFERENCE_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")


class AIServiceError(Exception):
    pass


async def _call_do_chat_completion(system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
    if not DO_API_KEY:
        raise AIServiceError("DIGITALOCEAN_INFERENCE_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
        "Content-Type": "application/json"
    }

    request_body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload)}
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient(timeout=12.0) as client:
        response = await client.post(DO_API_URL, headers=headers, json=request_body)

    if response.status_code >= 400:
        raise AIServiceError(f"Inference API error: {response.status_code} {response.text}")

    data = response.json()
    try:
        raw_content = data["choices"][0]["message"]["content"]
        return json.loads(raw_content)
    except Exception as exc:
        raise AIServiceError(f"Invalid inference response format: {exc}")


async def predict_eta(payload: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "You are a restaurant waitlist ETA prediction engine. "
        "Return strict JSON with keys: eta_minutes (int), confidence (0-1 float), source (string='ai')."
    )
    return await _call_do_chat_completion(system_prompt, payload)


async def score_no_show(payload: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "You are a no-show risk scoring engine for restaurant queues. "
        "Return strict JSON with keys: risk_score (0-1 float), risk_band ('low'|'medium'|'high'), "
        "recommended_action (string), source (string='ai')."
    )
    return await _call_do_chat_completion(system_prompt, payload)


async def staffing_recommendation(payload: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "You are a restaurant staffing insight engine. "
        "Return strict JSON with keys: peak_windows (array of strings), recommendation (string), "
        "projected_wait_reduction_minutes (float), source (string='ai')."
    )
    return await _call_do_chat_completion(system_prompt, payload)
