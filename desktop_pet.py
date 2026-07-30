"""Małe, zawsze widoczne okno pupila desktopowego."""

import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

from config import save_config


class DesktopPet:
    def __init__(self, config, agent):
        self.config = config
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("TotaPetAI")
        self.root.geometry("240x280")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#fff9f4")
        self._set_position()
        self._build_ui()
        self.root.bind("<ButtonPress-1>", self._drag_start)
        self.root.bind("<B1-Motion>", self._drag_move)
        self.root.bind("<ButtonRelease-1>", self._drag_end)

    def _build_ui(self):
        frame = tk.Frame(self.root, bg="#fff9f4", highlightbackground="#ffe2d4", highlightthickness=2)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        tk.Label(frame, text="TotaPetAI", bg="#fff9f4", fg="#756b82", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        tk.Button(frame, text="×", command=self.root.destroy, bg="#fff9f4", fg="#756b82", relief="flat").place(relx=1, x=-8, y=2, anchor="ne")
        tk.Label(frame, text="◕ᴗ◕", bg="#f5b9a8", fg="#241b35", font=("Segoe UI", 42), width=5, height=2).pack(pady=18)
        tk.Label(frame, text=f"Cześć! Jestem {self.config.pet_name}.", bg="#fff9f4", fg="#241b35", font=("Segoe UI", 11, "bold")).pack()
        tk.Label(frame, text="Przeciągnij mnie po pulpicie", bg="#fff9f4", fg="#756b82", font=("Segoe UI", 9)).pack(pady=4)
        tk.Button(frame, text="Porozmawiaj", command=self._talk, bg="#ff7a59", fg="white", relief="flat", padx=12).pack(pady=8)
        self.root.bind("<Button-3>", self._menu)

    def _set_position(self):
        if self.config.position_x is not None and self.config.position_y is not None:
            self.root.geometry(f"+{self.config.position_x}+{self.config.position_y}")
        else:
            self.root.update_idletasks()
            self.root.geometry(f"+{self.root.winfo_screenwidth() - 280}+{self.root.winfo_screenheight() - 350}")

    def _drag_start(self, event):
        self._drag_x, self._drag_y = event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y()

    def _drag_move(self, event):
        self.root.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    def _drag_end(self, _event):
        self.config.position_x, self.config.position_y = self.root.winfo_x(), self.root.winfo_y()
        save_config(self.config)

    def _talk(self):
        answer = self.agent.reply("Porozmawiaj ze mną i przedstaw się.")
        messagebox.showinfo(self.config.pet_name, answer, parent=self.root)

    def _menu(self, event):
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="Ustawienia", command=lambda: subprocess.Popen([sys.executable, __file__.replace("desktop_pet.py", "main.py"), "--ustawienia"]))
        menu.add_command(label="Wróć do domyślnej pozycji", command=self._reset_position)
        menu.add_separator()
        menu.add_command(label="Zamknij", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    def _reset_position(self):
        self.config.position_x = self.config.position_y = None
        save_config(self.config)
        self._set_position()

    def run(self):
        self.root.mainloop()
