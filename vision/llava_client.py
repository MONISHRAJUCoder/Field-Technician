import os
import base64
from typing import Optional

try:
    from huggingface_hub import InferenceApi
except Exception:
    InferenceApi = None

import requests


def detect_issue_llava(image_path: str, model: str = "llava-hf/llava-1.5-7b-hf", hf_token_env: str = "HF_API_TOKEN") -> str:
    """Call the Hugging Face LLaVA model to describe / detect what's in the image.

    The function first tries to use `huggingface_hub.InferenceApi` if available, otherwise
    falls back to the HF Inference HTTP API using `requests`.

    Requires a Hugging Face token available in the environment variable specified by
    `hf_token_env` (default `HF_API_TOKEN`).
    """
    hf_token = os.getenv(hf_token_env)
    if not hf_token:
        raise ValueError(f"Hugging Face token not set in env var {hf_token_env}")

    prompt = (
        "Please describe the main visible objects or issues in the image in a single short label."
    )

    # Try huggingface_hub InferenceApi when installed
    if InferenceApi is not None:
        try:
            api = InferenceApi(repo_id=model, token=hf_token)
            with open(image_path, "rb") as f:
                # Many vision-LM endpoints accept dict inputs with image and text
                payload = {"image": f, "text": prompt}
                res = api(payload)
            # The API may return a string or dict; prefer string
            if isinstance(res, (str,)):
                return res.strip()
            # If dict, try common fields
            if isinstance(res, dict):
                for k in ("generated_text", "text", "output", "answer"):
                    if k in res:
                        return str(res[k]).strip()
                return str(res)
        except Exception as e:
            # Fall through to HTTP fallback
            print(f"llava_client: huggingface_hub InferenceApi call failed: {e}")

    # Fallback: use HF Inference HTTP API
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "inputs": {"image": {"_type": "image_bytes", "data": b64}, "text": prompt}
    }
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"HF inference request failed: {e}")

    # Try parse JSON
    try:
        data = resp.json()
    except Exception:
        return resp.text.strip()

    # Common keys
    if isinstance(data, dict):
        for k in ("generated_text", "text", "output", "answer", "result"):
            if k in data:
                return str(data[k]).strip()
    if isinstance(data, list) and len(data) > 0:
        first = data[0]
        if isinstance(first, dict):
            for k in ("generated_text", "text", "answer"):
                if k in first:
                    return str(first[k]).strip()
        return str(first)

    return str(data)
