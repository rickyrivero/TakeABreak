import tkinter as tk
from config.settings_manager import save_settings

def popup_toggle(parent, settings):
    val = tk.BooleanVar(value=settings.get("show_popup", True))

    def toggle():
        settings["show_popup"] = val.get()
        save_settings(settings)

    tk.Checkbutton(
        parent,
        text="Show Popup",
        variable=val,
        command=toggle,
        bg="#2c3e50", fg="white",
        selectcolor="#34495e"
    ).pack(anchor='w', padx=10)

