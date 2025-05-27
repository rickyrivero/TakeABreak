from config.sound_player import play_sound
from config.settings_manager import load_settings
from config.popup_alert import show_popup

class CompleteTimer:
    def __init__(self, app, label):
        self.app = app
        self.label = label
        self.settings = load_settings()
        self.work_duration = self.settings.get("work_minutes", 25) * 60
        self.break_duration = self.settings.get("break_minutes", 5) * 60
        self.remaining = self.work_duration
        self.phase = "work"  # Alterna entre 'work' y 'break'
        self.running = False
        self.paused = False

    def start(self):
        self.running = True
        self.phase = "work"
        self.remaining = self.work_duration
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
        self.label.config(text=f"{self.phase.capitalize()} {mins:02d}:{secs:02d}")

        if self.remaining > 0:
            self.remaining -= 1
            self.label.after(1000, self.update)
        else:
            # ⏰ Alarma y popup al final de cada fase
            play_sound(self.settings["sound_file"], self.settings["sound_duration"])
            if self.settings.get("show_popup", True):
                if self.phase == "work":
                    show_popup("Break time!", "Step away and relax.")
                else:
                    show_popup("Work time!", "Back to focus mode!")

            # 🔁 Alternar entre fases automáticamente
            if self.phase == "work":
                self.phase = "break"
                self.remaining = self.break_duration
                self.update()
            else:
                self.phase = "work"
                self.remaining = self.work_duration
                self.update()

