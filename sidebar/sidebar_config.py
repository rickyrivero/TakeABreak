import tkinter as tk
from sidebar.mode_selector import mode_selector
from sidebar.popup_toggle import popup_toggle
from sidebar.sound_selector import sound_selector

class Sidebar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2c3e50", width=200)
        self.app = app
        self.settings = app.settings

        tk.Label(self, text="Settings", fg="white", bg="#2c3e50", font=("Arial", 14)).pack(pady=10)

        mode_selector(self, self.settings)
        popup_toggle(self, self.settings)
        sound_selector(self, self.settings)

        # Botón para cambiar entre claro / oscuro
        tk.Button(self, text="Toggle Theme", command=self.app.switch_theme).pack(pady=10)
