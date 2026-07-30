"""Punkt startowy TotaPetAI."""

import sys
from totapet.core.agent import Agent
from totapet.core.config import load_config
from totapet.integrations.telegram_bot import TelegramBot
from totapet.ui.desktop_pet import DesktopPet
from totapet.ui.settings_app import SettingsApp


def run_pet() -> None:
    config = load_config()
    agent = Agent(config)
    pet = DesktopPet(config, agent)
    telegram = TelegramBot(config, agent)
    telegram.start()
    pet.run()
    telegram.stop()


def main() -> None:
    if "--ustawienia" in sys.argv:
        SettingsApp(load_config()).run()
    else:
        run_pet()


if __name__ == "__main__":
    main()
