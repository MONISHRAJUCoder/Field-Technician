import os
import json
from typing import Optional

import requests


def detect_issue_via_endpoint(image_path: str, endpoint: Optional[str] = None, api_key_env: str = "QWEN_API_KEY") -> str:
    """Send an image to a remote model endpoint (e.g. Qwen-VL) and return the predicted label/text.

    This is a generic client that POSTs the image file as multipart/form-data to the given
    endpoint. The endpoint is expected to return JSON. It will try to extract a sensible
    text/label from common response fields.

    Configure the endpoint via the `QWEN_ENDPOINT` env var or pass `endpoint` directly.
    Provide an API key via the `QWEN_API_KEY` env var if the endpoint requires authorization.
    """
    endpoint = endpoint or os.getenv("QWEN_ENDPOINT")
    if not endpoint:
        raise ValueError("No endpoint provided and QWEN_ENDPOINT not set")

    api_key = os.getenv(api_key_env)
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    with open(image_path, "rb") as f:
        files = {"image": (os.path.basename(image_path), f, "application/octet-stream")}
        try:
            resp = requests.post(endpoint, headers=headers, files=files, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Request to endpoint failed: {e}")

    # Parse JSON response
    try:
        data = resp.json()
    except json.JSONDecodeError:
        # If the endpoint returns plain text, return it directly
        return resp.text.strip()

    # Try common keys
    for key in ("label", "prediction", "predictions", "text", "result", "output", "answer"):
        if key in data:
            val = data[key]
            # If predictions is a list, pick first element's text/label if present
            if isinstance(val, list) and len(val) > 0:
                first = val[0]
                if isinstance(first, dict):
                    for sub in ("label", "text", "answer", "prediction"):
                        if sub in first:
                            return str(first[sub])
                return str(first)
            return str(val)

    # Fallback: return entire JSON as string for debugging
    return json.dumps(data)
