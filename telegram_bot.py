"""Integracja z Telegram Bot API przez long polling."""

import json
import threading
import urllib.parse
import urllib.request


class TelegramBot:
    def __init__(self, config, agent):
        self.config = config
        self.agent = agent
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if not self.config.telegram_token:
            return
        self._thread = threading.Thread(target=self._poll, daemon=True, name="telegram-bot")
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _api(self, method: str, values: dict) -> dict:
        url = f"https://api.telegram.org/bot{self.config.telegram_token}/{method}"
        data = urllib.parse.urlencode(values).encode()
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))

    def _poll(self) -> None:
        offset = 0
        while not self._stop.is_set():
            try:
                result = self._api("getUpdates", {"timeout": 25, "offset": offset})
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat = message.get("chat", {})
                    text = message.get("text")
                    if not text or not self._allowed(chat.get("id")):
                        continue
                    self._api("sendMessage", {"chat_id": chat["id"], "text": self.agent.reply(text)})
            except (OSError, ValueError, KeyError):
                self._stop.wait(5)

    def _allowed(self, chat_id) -> bool:
        return not self.config.telegram_allowed_user or str(chat_id) == self.config.telegram_allowed_user.strip()
