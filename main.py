"""Punkt startowy TotaPetAI."""

import sys
import tkinter as tk

from agent import Agent
from config import load_config
from desktop_pet import DesktopPet
from settings_app import SettingsApp
from telegram_bot import TelegramBot


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
