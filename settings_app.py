"""Polskie okno konfiguracji TotaPetAI."""

import tkinter as tk
from tkinter import messagebox

from config import save_config


class SettingsApp:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.root.title("Ustawienia TotaPetAI")
        self.root.geometry("560x510")
        self.root.minsize(480, 450)
        self.root.configure(bg="#fff9f4")
        self.fields = {}
        self._build()

    def _build(self):
        tk.Label(self.root, text="Ustawienia TotaPetAI", bg="#fff9f4", fg="#241b35", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=28, pady=(22, 4))
        tk.Label(self.root, text="Skonfiguruj rozmowę AI i opcjonalnego bota Telegram.", bg="#fff9f4", fg="#756b82", font=("Segoe UI", 10)).pack(anchor="w", padx=28, pady=(0, 16))
        form = tk.Frame(self.root, bg="#fff9f4")
        form.pack(fill="both", expand=True, padx=28)
        fields = [("Adres API LLM", "llm_url"), ("Model", "llm_model"), ("Klucz API LLM", "llm_api_key"), ("Token bota Telegram", "telegram_token"), ("Dozwolony identyfikator Telegram", "telegram_allowed_user"), ("Nazwa pupila", "pet_name")]
        for row, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg="#fff9f4", fg="#241b35", font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=5)
            variable = tk.StringVar(value=str(getattr(self.config, key)))
            entry = tk.Entry(form, textvariable=variable, width=54, show="*" if "key" in key or "token" in key else "")
            entry.grid(row=row, column=1, sticky="ew", padx=(18, 0), pady=5)
            self.fields[key] = variable
        form.columnconfigure(1, weight=1)
        tk.Label(form, text="Instrukcja systemowa agenta", bg="#fff9f4", fg="#241b35", font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="nw", pady=5)
        self.prompt = tk.Text(form, width=40, height=5, wrap="word")
        self.prompt.insert("1.0", self.config.system_prompt)
        self.prompt.grid(row=6, column=1, sticky="ew", padx=(18, 0), pady=5)
        tk.Button(self.root, text="Zapisz ustawienia", command=self._save, bg="#ff7a59", fg="white", relief="flat", padx=18, pady=8).pack(anchor="e", padx=28, pady=18)

    def _save(self):
        for key, variable in self.fields.items():
            setattr(self.config, key, variable.get().strip())
        self.config.system_prompt = self.prompt.get("1.0", "end").strip()
        save_config(self.config)
        messagebox.showinfo("Zapisano", "Ustawienia zostały zapisane.", parent=self.root)

    def run(self):
        self.root.mainloop()
