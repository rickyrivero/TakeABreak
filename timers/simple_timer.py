from config.sound_player import play_sound
from config.settings_manager import load_settings

class SimpleTimer:
    def __init__(self, app, label):
        self.app = app
        self.label = label
        self.settings = load_settings()
        self.duration = self.settings.get("cycle_minutes", 25) * 60
        self.remaining = self.duration
        self.running = False
        self.paused = False

    def start(self):
        self.running = True
        self.update()

    def pause(self):
        self.paused = True

    def resume(self):
        if self.running and self.paused:
            self.paused = False
            self.update()

    def update(self):
        if not self.running or self.paused:
            return
        mins, secs = divmod(self.remaining, 60)
        self.label.config(text=f"{mins:02d}:{secs:02d}")
        if self.remaining > 0:
            self.remaining -= 1
            self.label.after(1000, self.update)
        else:
            play_sound(self.settings["sound_file"], self.settings["sound_duration"])
            self.label.config(text="Done!")
            self.running = False
            # ✅ Mostrar popup si está activado
            if self.settings.get("show_popup", True):
                from config.popup_alert import show_popup
                show_popup("Time's up!", "Take a break or stretch!")

            self.label.config(text="Done!")
            self.running = False