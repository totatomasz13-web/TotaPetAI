"""Prosty agent rozmowy z lokalnymi narzędziami."""

from datetime import datetime
import threading

from llm_client import LLMError, ask_llm


class Agent:
    def __init__(self, config):
        self.config = config
        self._lock = threading.Lock()
        self._history: list[dict[str, str]] = []

    def reply(self, text: str) -> str:
        command = text.strip().lower()
        if command in {"/pomoc", "pomoc"}:
            return "Mogę rozmawiać przez LLM. Komendy: /pomoc, /czas, /wyczyść."
        if command in {"/czas", "która godzina"}:
            return f"Jest teraz {datetime.now().strftime('%H:%M')}."
        if command == "/wyczyść":
            with self._lock:
                self._history.clear()
            return "Wyczyściłem naszą rozmowę."

        with self._lock:
            messages = [{"role": "system", "content": self.config.system_prompt}]
            messages.extend(self._history[-12:])
            messages.append({"role": "user", "content": text})
            try:
                answer = ask_llm(self.config, messages)
            except LLMError as error:
                return str(error)
            self._history.extend([{"role": "user", "content": text}, {"role": "assistant", "content": answer}])
            return answer
