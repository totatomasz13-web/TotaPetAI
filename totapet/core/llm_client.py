"""Lekki klient API LLM bez obowiązkowej biblioteki zewnętrznej."""

import json
import urllib.error
import urllib.request


class LLMError(RuntimeError):
    pass


def ask_llm(config, messages: list[dict[str, str]]) -> str:
    if not config.llm_api_key:
        return "Nie mam jeszcze klucza API LLM. Otwórz ustawienia i uzupełnij go, żebym mógł rozmawiać."

    body = json.dumps({"model": config.llm_model, "messages": messages, "temperature": 0.7}).encode()
    request = urllib.request.Request(
        config.llm_url,
        data=body,
        headers={"Authorization": f"Bearer {config.llm_api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as error:
        raise LLMError(f"Nie udało się połączyć z API LLM: {error}") from error
