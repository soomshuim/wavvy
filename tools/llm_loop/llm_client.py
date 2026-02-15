"""Minimal OpenAI client without external SDK dependency."""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from urllib import error, request


class LLMClientError(RuntimeError):
    """Raised when provider call fails."""


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    temperature: float
    api_key: str


def generate_text(cfg: LLMConfig, prompt: str) -> str:
    if cfg.provider != "openai":
        raise LLMClientError(f"Unsupported provider: {cfg.provider}")
    if not cfg.api_key:
        raise LLMClientError("OPENAI_API_KEY is missing.")

    payload = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": "You are a precise production assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    # Some models reject non-default temperature; only include when it differs
    # from default and is known-safe for general chat completions usage.
    if abs(cfg.temperature - 1.0) > 1e-9 and not cfg.model.startswith("gpt-5"):
        payload["temperature"] = cfg.temperature
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url="https://api.openai.com/v1/chat/completions",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg.api_key}",
        },
    )
    try:
        with request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise LLMClientError(f"OpenAI HTTP {exc.code}: {details}") from exc
    except error.URLError as exc:
        raise LLMClientError(f"Network error: {exc}") from exc
    except TimeoutError as exc:
        raise LLMClientError(f"Timeout: {exc}") from exc
    except socket.timeout as exc:
        raise LLMClientError(f"Timeout: {exc}") from exc

    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # pragma: no cover
        raise LLMClientError(f"Unexpected response shape: {data}") from exc
