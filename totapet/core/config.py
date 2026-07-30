"""Konfiguracja aplikacji zapisywana lokalnie w profilu użytkownika."""

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path


APP_DIR = Path(os.environ.get("APPDATA", Path.home())) / "TotaPetAI"
CONFIG_FILE = APP_DIR / "config.json"


@dataclass
class Config:
    llm_url: str = "https://api.openai.com/v1/chat/completions"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""
    telegram_token: str = ""
    telegram_allowed_user: str = ""
    pet_name: str = "Tota"
    system_prompt: str = (
        "Jesteś Totą, sympatycznym polskim pupilem AI na pulpit. "
        "Odpowiadasz krótko, ciepło i konkretnie. Nie udzielasz diagnoz medycznych."
    )
    position_x: int | None = None
    position_y: int | None = None


def load_config() -> Config:
    config = Config()
    try:
        values = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        config = Config(**{key: value for key, value in values.items() if key in Config.__annotations__})
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        pass
    config.llm_api_key = os.environ.get("LLM_API_KEY", config.llm_api_key)
    config.llm_url = os.environ.get("LLM_URL", config.llm_url)
    config.llm_model = os.environ.get("LLM_MODEL", config.llm_model)
    config.telegram_token = os.environ.get("TELEGRAM_TOKEN", config.telegram_token)
    config.telegram_allowed_user = os.environ.get("TELEGRAM_ALLOWED_USER", config.telegram_allowed_user)
    return config


def save_config(config: Config) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(asdict(config), ensure_ascii=False, indent=2), encoding="utf-8")
