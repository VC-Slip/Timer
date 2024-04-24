import tkinter as tk
import time
import pickle


class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")

        self.is_paused = False
        self.time_label = tk.Label(master, text="0000:00:00", font=("Helvetica", 48))
        self.time_label.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Pause", command=self.stop_timer)
        self.stop_button.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        try:
            with open("timer_state.pickle", "rb") as file:
                self.start_time, self.elapsed_time = pickle.load(file)
        except FileNotFoundError:
            pass

        self.update_timer()

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            self.update_timer()
        else:
            self.is_paused = True

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.time_label.config(text="0000:00:00")

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        if self.elapsed_time < 3600:  # Less than an hour, show minutes and seconds only
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            time_string = "{:02d}:{:02d}".format(minutes, seconds)
        else:
            hours = int(self.elapsed_time // 3600)
            minutes = int((self.elapsed_time % 3600) // 60)
            seconds = int(self.elapsed_time % 60)
            time_string = "{:04d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        self.time_label.config(text=time_string)
        if self.running:
            self.master.after(1000, self.update_timer)

    def on_closing(self):
        self.save_state()
        self.master.destroy()

    def save_state(self):
        with open("timer_state.pickle", "wb") as file:
            pickle.dump((self.start_time, self.elapsed_time), file)


def main():
    root = tk.Tk()
    timer_app = TimerApp(root)
    root.protocol("WM_DELETE_WINDOW", timer_app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
