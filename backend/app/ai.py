import json
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from .config import get_settings


class ProviderError(RuntimeError):
    pass


def _post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, headers={
        "Content-Type": "application/json",
        **(headers or {}),
    }, method="POST")
    try:
        with urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except (URLError, HTTPError, TimeoutError, ValueError) as exc:
        raise ProviderError(f"AI provider request failed: {exc}") from exc


def chat(messages: list[dict]) -> tuple[str, str]:
    settings = get_settings()
    if settings.ai_api_key.strip():
        base = settings.ai_base_url.rstrip("/")
        result = _post_json(
            f"{base}/chat/completions",
            {"model": settings.ai_model, "messages": messages, "temperature": 0.4},
            {"Authorization": f"Bearer {settings.ai_api_key.strip()}"},
        )
        try:
            return result["choices"][0]["message"]["content"], "cloud"
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Cloud provider returned an unexpected response.") from exc

    base = settings.ollama_base_url.rstrip("/")
    prompt_messages = messages
    result = _post_json(
        f"{base}/api/chat",
        {"model": settings.ollama_model, "messages": prompt_messages, "stream": False},
    )
    try:
        return result["message"]["content"], "ollama"
    except (KeyError, TypeError) as exc:
        raise ProviderError("Ollama returned an unexpected response.") from exc
