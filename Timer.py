from tkinter import Tk, Button, Label, messagebox, Toplevel, Entry
import time
import pickle


class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")

        self.is_paused = False
        self.time_label = Label(master, text="0000:00:00", font=("Helvetica", 48))
        self.time_label.pack()

        self.start_button = Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.dev_button = Button(master, text="Developer Options", command=self.open_dev_options)
        self.dev_button.pack()

        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        self.default_hours = 0
        self.default_minutes = 0
        self.default_seconds = 0

        self.hours_entry = Entry(width=5)
        self.minutes_entry = Entry(width=5)
        self.seconds_entry = Entry(width=5)

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

    def pause_timer(self):
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

    def change_time(self, hours, minutes, seconds):
        self.default_hours = hours
        self.default_minutes = minutes
        self.default_seconds = seconds
        self.elapsed_time = hours * 3600 + minutes * 60 + seconds

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

    def open_dev_options(self):
        if messagebox.askyesno("Developer Options",
                               "Are you sure you want to open developer options? This is for developers only."):
            dev_window = Toplevel(self.master)
            dev_window.title("Developer Options")

            Label(dev_window, text="Adjust Timer Time").pack()

            Label(dev_window, text="Hours:").pack()
            self.hours_entry = Entry(dev_window, width=5)
            self.hours_entry.insert(0, str(self.default_hours))
            self.hours_entry.pack()

            Label(dev_window, text="Minutes:").pack()
            self.minutes_entry = Entry(dev_window, width=5)
            self.minutes_entry.insert(0, str(self.default_minutes))
            self.minutes_entry.pack()

            Label(dev_window, text="Seconds:").pack()
            self.seconds_entry = Entry(dev_window, width=5)
            self.seconds_entry.insert(0, str(self.default_seconds))
            self.seconds_entry.pack()

            Button(dev_window, text="Apply", command=self.apply_dev_changes).pack()

    def apply_dev_changes(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.change_time(hours=hours, minutes=minutes, seconds=seconds)
            messagebox.showinfo("Success", "Timer time has been adjusted successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for hours, minutes, and seconds.")

    def on_closing(self):
        self.save_state()
        self.master.destroy()

    def save_state(self):
        with open("timer_state.pickle", "wb") as file:
            pickle.dump((self.start_time, self.elapsed_time), file)


def main():
    root = Tk()
    timer_app = TimerApp(root)
    root.protocol("WM_DELETE_WINDOW", timer_app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
