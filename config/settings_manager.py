import json
import os

SETTINGS_PATH = "config.json"

default_settings = {
    "mode": "simple",
    "show_popup": True,
    "sound_file": "assets/alarm.mp3",
    "sound_duration": 10,
    "theme": "light",
    "work_minutes": 25,
    "break_minutes": 5
}

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                data = json.load(f)
                for key, value in default_settings.items():
                    data.setdefault(key, value)
                return data
        except Exception as e:
            print(f"[ERROR loading settings] {e}")
            return default_settings.copy()
    else:
        save_settings(default_settings)
        return default_settings.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"[ERROR saving settings] {e}")

