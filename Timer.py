from tkinter import Tk, Button, Label, messagebox, Toplevel, Entry
import time
import pickle
import logging


# Set up logging to both file and console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = logging.FileHandler("timer_app_debug.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")

        # Log the initialization
        logging.debug("Timer app initialized.")

        self.is_paused = False
        self.time_label = Label(master, text="0000:00:00", font=("Helvetica", 48))
        self.time_label.pack()

        self.start_button = Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.reset_button = Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

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

        self.state_file_path = "E:/Pycharm Projects/Timer/Timer_App/timer_state.pickle"
        logging.debug(f"State file path: {self.state_file_path}")

        try:
            with open(self.state_file_path, "rb") as file:
                self.start_time, self.elapsed_time = pickle.load(file)
            logging.debug(f"Loaded state from pickle: start_time={self.start_time}, elapsed_time={self.elapsed_time}")
        except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
            logging.error(f"Error loading state file: {e}. Using default values.")
            self.start_time = None
            self.elapsed_time = 0

        self.update_timer()
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            logging.debug(f"Timer started. start_time={self.start_time}")
            self.update_timer()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            logging.debug(f"Timer paused. elapsed_time={self.elapsed_time}")
            self.update_timer()
        else:
            self.is_paused = True
            logging.debug("Timer was already paused.")

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        logging.debug("Timer reset.")
        self.update_timer()

    def change_time(self, hours, minutes, seconds):
        self.default_hours = hours
        self.default_minutes = minutes
        self.default_seconds = seconds
        self.elapsed_time = max(0,hours * 3600 + minutes * 60 + seconds)
        logging.debug(f"Time changed to: {self.default_hours}h {self.default_minutes}m {self.default_seconds}s")

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
            time_string = "{}:{:02d}:{:02d}".format(hours, minutes, seconds)

        self.time_label.config(text=time_string)
        if self.running:
            self.master.after(1000, self.update_timer)

    def open_dev_options(self):
        if messagebox.askyesno("Developer Options",
                               "Are you sure you want to open developer options? This is for developers only."):
            logging.debug("Entering developer options")
            dev_window = Toplevel(self.master)
            dev_window.title("Developer Options")

            Label(dev_window, text="Adjust Timer Time").pack()

            Label(dev_window, text="Hours:").pack()
            self.hours_entry = Entry(dev_window, width=5)
            self.hours_entry.pack()

            Label(dev_window, text="Minutes:").pack()
            self.minutes_entry = Entry(dev_window, width=5)
            self.minutes_entry.pack()

            Label(dev_window, text="Seconds:").pack()
            self.seconds_entry = Entry(dev_window, width=5)
            self.seconds_entry.pack()

            Button(dev_window, text="Apply", command=lambda: self.apply_dev_changes(dev_window)).pack()

    def apply_dev_changes(self, dev_window):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())

            self.change_time(hours=hours, minutes=minutes, seconds=seconds)

            self.update_timer()

            logging.debug(f"Developer changes applied: {hours}h {minutes}m {seconds}s")
            messagebox.showinfo("Success", "Timer time has been adjusted successfully!")

            dev_window.destroy()
        except ValueError:
            logging.error("Invalid input for hours, minutes, or seconds.")
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for hours, minutes, and seconds.")

    def on_closing(self):
        self.save_state()
        logging.debug("App closing, state saved.")
        self.master.destroy()

    def save_state(self):
        logging.debug("saving state to:{self.sate_file_path}")
        try:
            with open(self.state_file_path, "wb") as pickle_file:
                pickle.dump((self.start_time, self.elapsed_time), pickle_file)
                logging.debug("State saved successfully.")
        except Exception as e:
            logging.error(f"Error saving state: {e}")


def main():
    root = Tk()
    timer_app = TimerApp(root)
    root.protocol("WM_DELETE_WINDOW", timer_app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
