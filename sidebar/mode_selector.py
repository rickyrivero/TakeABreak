import tkinter as tk
from config.settings_manager import save_settings

def mode_selector(parent, settings):
    mode = tk.StringVar(value=settings["mode"])

    def update_mode():
        settings["mode"] = mode.get()
        save_settings(settings)
        # Refrescar UI al cambiar el modo
        parent.app.mode = mode.get()
        parent.app.render_duration_fields()

    tk.Label(parent, text="Mode:", bg="#2c3e50", fg="white").pack()
    for opt in ["simple", "complete"]:
        tk.Radiobutton(
            parent,
            text=opt.capitalize(),
            variable=mode,
            value=opt,
            bg="#2c3e50",
            fg="white",
            selectcolor="#34495e",
            command=update_mode
        ).pack(anchor='w', padx=20)

