import tkinter as tk
from sidebar.sidebar_config import Sidebar
from timers.simple_timer import SimpleTimer
from timers.complete_timer import CompleteTimer
from config.settings_manager import load_settings, save_settings

class TakeABreakApp:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.settings["mode"]
        self.theme = self.settings.get("theme", "light")

        self.root.title("Take A Break")
        self.root.geometry("700x420")
        self.root.configure(bg=self.get_bg())

        # Sidebar
        self.sidebar = Sidebar(root, self)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Main interface
        self.main = tk.Frame(root, bg=self.get_bg())
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.timer_label = tk.Label(self.main, text="00:00", font=("Arial", 32), bg=self.get_bg(), fg=self.get_fg())
        self.timer_label.pack(pady=20)

        # Inputs
        self.cycle_entry = None
        self.work_entry = None
        self.break_entry = None
        self.input_container = tk.Frame(self.main, bg=self.get_bg())
        self.input_container.pack()

        self.render_duration_fields()

        # Buttons
        self.start_btn = tk.Button(self.main, text="Start", command=self.start_timer)
        self.start_btn.pack(pady=5)

        self.pause_btn = tk.Button(self.main, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_btn.pack(pady=5)

        self.resume_btn = tk.Button(self.main, text="Resume", command=self.resume_timer, state=tk.DISABLED)
        self.resume_btn.pack(pady=5)

        self.reset_btn = tk.Button(self.main, text="Reset", command=self.reset_timer)
        self.reset_btn.pack(pady=5)


        self.timer = None

    def get_bg(self):
        return "#ffffff" if self.theme == "light" else "#1e1e1e"

    def get_fg(self):
        return "#000000" if self.theme == "light" else "#ffffff"

    def apply_theme(self):
        bg = self.get_bg()
        fg = self.get_fg()
        entry_bg = "#2e2e2e" if self.theme == "dark" else "white"
        entry_fg = "#ffffff" if self.theme == "dark" else "#000000"

        self.root.configure(bg=bg)
        self.main.configure(bg=bg)
        self.timer_label.configure(bg=bg, fg=fg)
        self.start_btn.configure(bg=bg, fg=fg)
        self.pause_btn.configure(bg=bg, fg=fg)
        self.resume_btn.configure(bg=bg, fg=fg)

        # Aplicar tema a los inputs según el modo
        if self.settings["mode"] == "simple" and self.cycle_entry:
            self.cycle_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
        elif self.settings["mode"] == "complete":
            if self.work_entry:
                self.work_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            if self.break_entry:
                self.break_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)


    def switch_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.settings["theme"] = self.theme
        save_settings(self.settings)
        self.apply_theme()

    def render_duration_fields(self):
        for widget in self.input_container.winfo_children():
            widget.destroy()

        self.mode = self.settings.get("mode", "simple")

        if self.mode == "simple":
            tk.Label(self.input_container, text="Cycle duration (min)", bg=self.get_bg(), fg=self.get_fg()).pack()
            self.cycle_entry = tk.Entry(self.input_container, width=10, justify="center")
            self.cycle_entry.insert(0, str(self.settings.get("cycle_minutes", 25)))
            self.cycle_entry.pack()

        elif self.mode == "complete":
            tk.Label(self.input_container, text="Work minutes", bg=self.get_bg(), fg=self.get_fg()).pack()
            self.work_entry = tk.Entry(self.input_container, width=10, justify="center")
            self.work_entry.insert(0, str(self.settings.get("work_minutes", 25)))
            self.work_entry.pack()

            tk.Label(self.input_container, text="Break minutes", bg=self.get_bg(), fg=self.get_fg()).pack()
            self.break_entry = tk.Entry(self.input_container, width=10, justify="center")
            self.break_entry.insert(0, str(self.settings.get("break_minutes", 5)))
            self.break_entry.pack()

    def start_timer(self):
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)

        try:
            if self.settings["mode"] == "simple":
                self.settings["cycle_minutes"] = int(self.cycle_entry.get())
            else:
                self.settings["work_minutes"] = int(self.work_entry.get())
                self.settings["break_minutes"] = int(self.break_entry.get())
            save_settings(self.settings)
        except:
            print("Invalid input")
            return

        self.mode = self.settings.get("mode", "simple")
        if self.mode == "simple":
            self.timer = SimpleTimer(self, self.timer_label)
        else:
            self.timer = CompleteTimer(self, self.timer_label)
        self.timer.start()

    def pause_timer(self):
        if self.timer:
            self.timer.pause()
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)

    def resume_timer(self):
        if self.timer:
            self.timer.resume()
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)

    def reset_timer(self):
        if self.timer:
            self.timer.running = False
            self.timer.paused = False
            self.timer = None

        try:
            if self.settings["mode"] == "simple":
                self.settings["cycle_minutes"] = int(self.cycle_entry.get())
                mins = self.settings["cycle_minutes"]
                self.timer_label.config(text=f"{mins:02d}:00")

            elif self.settings["mode"] == "complete":
                self.settings["work_minutes"] = int(self.work_entry.get())
                self.settings["break_minutes"] = int(self.break_entry.get())

                # Detectar fase actual del timer, si existe
                phase = "work"
                if hasattr(self.timer, "phase"):
                    phase = self.timer.phase

                if phase == "work":
                    mins = self.settings["work_minutes"]
                    self.timer_label.config(text=f"Work {mins:02d}:00")
                else:
                    mins = self.settings["break_minutes"]
                    self.timer_label.config(text=f"Break {mins:02d}:00")

            save_settings(self.settings)
        except:
            print("Invalid input on reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TakeABreakApp(root)
    root.mainloop()
