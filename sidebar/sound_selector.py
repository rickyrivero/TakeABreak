import tkinter as tk
from tkinter import filedialog
from config.settings_manager import save_settings

def sound_selector(parent, settings):
    def select_file():
        file = filedialog.askopenfilename(
            title="Choose Sound",
            filetypes=[("Audio", "*.mp3 *.wav")]
        )
        if file:
            settings["sound_file"] = file
            save_settings(settings)

    tk.Button(parent, text="Select Sound", command=select_file).pack(pady=5)

    tk.Label(parent, text="Sound Duration (sec):", bg="#2c3e50", fg="white").pack()
    entry = tk.Entry(parent)
    entry.insert(0, str(settings.get("sound_duration", 10)))
    entry.pack()

    def update():
        try:
            settings["sound_duration"] = int(entry.get())
            save_settings(settings)
        except:
            pass

    entry.bind("<FocusOut>", lambda e: update())

