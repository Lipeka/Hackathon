import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from flask import Flask
from flask_bcrypt import Bcrypt

class User:
    def __init__(self, username, password, timezone):
        self.username = username
        self.password = password
        self.timezone = timezone

class Authentication:
    def __init__(self):
        self.users = []
        self.add_user(User("admin", "admin123", timezone('US/Eastern')))

    def add_user(self, user):
        self.users.append(user)

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

class SmartBoard:
    def __init__(self):
        self.end_of_hour_indicator = False
        self.next_hour_subject = ""
        self.next_hour_faculty = ""
        self.schedule = {
            'Monday': {'subjects': ['Math', 'Physics', 'Chem', 'Lunch', 'Comp.Sci/Bio', 'Eng', 'PT', 'PT'],
                       'faculties': ['Mr. A', 'Ms. B', 'Mr.c', 'Mr.A', 'Ms.Ab/Mr.xyz', 'Mr.D', 'Mr.PT']},
            'Tuesday': {'subjects': ['Physics', 'Chem', 'Comp.Sci/Bio', 'Lunch', 'Math', 'Eng', 'Eng', 'History'],
                        'faculties': ['Mr. A', 'Ms. B', 'Ms.AB/Mr.xyz', 'Mr.A', 'Ms.Ab', 'Mr.D', 'Mr.PT']},
            'Wednesday': {'subjects': ['Chem', 'Lang', 'Lang', 'Lunch', 'Comp.Sci/Bio', 'Eng', 'Math', 'Math'],
                          'faculties': ['Mr. A', 'Ms. B', 'Mr.c', 'Mr.A', 'Ms.Ab/Mr.xyz', 'Mr.D', 'Mr.PT']},
            'Thursday': {'subjects': ['Eng', 'Comp.sci/Bio', 'Chem', 'Lunch', 'Comp.Sci/Bio', 'Vocational', 'History',
                                      'Math'],
                         'faculties': ['Mr. A', 'Ms. B', 'Mr.c', 'Mr.A', 'Ms.Ab/Mr.xyz', 'Mr.D', 'Mr.PT']},
            'Friday': {'subjects': ['Math', 'Physics', 'Physics', 'Lunch', 'Comp.Sci/Bio', 'Chem', 'Chem', 'Math'],
                       'faculties': ['Mr. A', 'Ms. B', 'Mr.c', 'Mr.A', 'Ms.Ab/Mr.xyz', 'Mr.D', 'Mr.PT']},
        }
        self.notes_file_path = 'saved_notes.txt'
        self.notes = []

    def start_timer(self):
        now = datetime.now()
        if now.weekday() < 5 and 8 <= now.hour < 16:
            end_of_day_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
            duration_seconds = (end_of_day_time - now).total_seconds()
            timer_thread = threading.Timer(duration_seconds, self.trigger_end_of_hour)
            timer_thread.start()
            self.schedule_hourly_alerts()

    def trigger_end_of_hour(self):
        self.end_of_hour_indicator = True
        print("End of Hour Indicator Activated!")
        print(f"Next Hour Subject: {self.next_hour_subject}")
        print(f"Next Hour Faculty: {self.next_hour_faculty}")

    def update_schedule(self, day, subjects, faculties):
        if day in self.schedule:
            self.schedule[day]['subjects'].append(subjects)
            self.schedule[day]['faculties'].append(faculties)
        else:
            print("Invalid day.")

    def add_subject_faculty(self, day, subject, faculty):
        if day in self.schedule:
            self.schedule[day]['subjects'].append(subject)
            self.schedule[day]['faculties'].append(faculty)
        else:
            print("Invalid day.")

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes_to_file()

    def retrieve_notes(self):
        try:
            with open(self.notes_file_path, 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def save_notes_to_file(self):
        with open(self.notes_file_path, 'w') as file:
            for note in self.notes:
                file.write(note + '\n')

    def get_schedule_for_day(self, day):
        return self.schedule.get(day, {'subjects': [], 'faculties': []})

    def schedule_hourly_alerts(self):
        current_time = datetime.now().replace(second=0, microsecond=0)
        for hour in range(8, 17):
            alert_time = current_time.replace(hour=hour)
            if current_time <= alert_time <= current_time.replace(hour=16):
                next_hour = hour + 1
                day = datetime.now().strftime("%A")
                schedule = self.get_schedule_for_day(day)
                if next_hour < len(schedule['subjects']):
                    alert_time = current_time.replace(hour=hour)
                    time_difference = (alert_time - current_time).total_seconds()
                    threading.Timer(time_difference, self.display_hourly_alert, args=[next_hour]).start()

    def display_hourly_alert(self, hour):
        next_hour = hour + 1
        day = datetime.now().strftime("%A")
        schedule = self.get_schedule_for_day(day)
        if next_hour < len(schedule['subjects']):
            self.next_hour_subject = schedule['subjects'][next_hour]
            self.next_hour_faculty = schedule['faculties'][next_hour]
            notification_title = f"Next Hour Alert - {next_hour}:00 PM"
            notification_message = f"Subject: {self.next_hour_subject}\nFaculty: {self.next_hour_faculty}"
            notification_manager.send_notification(notification_title, notification_message)
            print("\a")

class NotificationManager:
    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Smart Board App",
        )

class AutomatedTasks:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.perform_automated_task, 'interval', minutes=30)
        self.scheduler.start()

    def perform_automated_task(self):
        print("Performing automated task...")

# Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)
auth = Authentication()
smart_board = SmartBoard()
notification_manager = NotificationManager()
automated_tasks = AutomatedTasks()

# Tkinter GUI
class SmartBoardApp:
    def __init__(self, root, smart_board):
        self.root = root
        self.smart_board = smart_board
        self.root.title("Smart Board App")

        welcome_label = tk.Label(root, text="Welcome to Smart Board App!", font=('Helvetica', 16))
        welcome_label.pack(pady=(10, 0))

        self.date_time_label = tk.Label(root, text="", font=('Helvetica', 12))
        self.date_time_label.pack(pady=(0, 10))

        self.current_hour_label = tk.Label(root, text="", font=('Helvetica', 12))
        self.current_hour_label.pack(pady=(0, 10))

        self.update_date_time()
        self.update_current_hour()

        self.schedule_frame = ttk.Frame(root)
        self.schedule_frame.pack(pady=10)
        self.add_widgets_to_schedule_frame()

        self.notes_frame = ttk.Frame(root)
        self.notes_frame.pack(pady=10)
        self.add_widgets_to_notes_frame()

    def update_date_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=f"Current Date/Time: {current_time}")
        self.root.after(1000, self.update_date_time)

    def update_current_hour(self):
        current_day = datetime.now().strftime("%A")
        current_hour = datetime.now().hour

        if current_day in self.smart_board.schedule:
            schedule = self.smart_board.get_schedule_for_day(current_day)
            self.display_current_subject_faculty(schedule, current_hour)
        else:
            self.current_hour_label.config(text="No Schedule Available!")

        self.root.after(1000 * 60 * 5, self.update_current_hour)

    def display_current_subject_faculty(self, schedule, current_hour):
        if current_hour < len(schedule['subjects']):
            current_subject = schedule['subjects'][current_hour]
            current_faculty = schedule['faculties'][current_hour]

            current_info_text = f"Current Hour: {current_subject}\nFaculty: {current_faculty}"
            self.current_hour_label.config(text=current_info_text)
        else:
            self.current_hour_label.config(text="School Hours Over!")

    def add_widgets_to_schedule_frame(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        timings = [f"{hour}:00 - {hour + 1}:00" for hour in range(8, 15)]

        for timing in timings:
            timing_label = tk.Label(self.schedule_frame, text=timing)
            timing_label.grid(row=timings.index(timing) + 1, column=0, padx=10, pady=5)

        for day in days:
            day_label = tk.Label(self.schedule_frame, text=day)
            day_label.grid(row=0, column=days.index(day) + 1, padx=10, pady=5)
            schedule = self.smart_board.get_schedule_for_day(day)

            min_length = min(len(schedule['subjects']), len(schedule['faculties']))

            for hour in range(min_length):
                subject = schedule['subjects'][hour]
                faculty = schedule['faculties'][hour]

                subject_label = tk.Label(self.schedule_frame, text=f"{subject}\n{faculty}")
                subject_label.grid(row=hour + 1, column=days.index(day) + 1, padx=10, pady=5)

    def add_widgets_to_notes_frame(self):
        add_note_button = tk.Button(self.notes_frame, text="Click to Write Notes", command=self.open_notes_window)
        add_note_button.grid(row=2, column=0, pady=10)

        retrieve_notes_button = tk.Button(self.notes_frame, text="Retrieve Notes", command=self.retrieve_notes_window)
        retrieve_notes_button.grid(row=2, column=1, pady=10)

    def open_notes_window(self):
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Write Notes")

        notes_label = tk.Label(notes_window, text="Enter your note:")
        notes_label.pack(pady=5)

        notes_text = tk.Text(notes_window, height=33, width=155)
        notes_text.pack(pady=10)

        save_button = tk.Button(notes_window, text="Save Notes", command=lambda: self.save_notes(notes_text))
        save_button.pack(pady=10)

    def open_note_details(self, notes_listbox):
        selected_index = notes_listbox.curselection()
        if selected_index:
            note_details_window = tk.Toplevel(self.root)
            note_details_window.title("Note Details")

            selected_note = notes_listbox.get(selected_index)
            note_label = tk.Label(note_details_window, text=selected_note, font=('Helvetica', 12))
            note_label.pack(padx=10, pady=5)

    def retrieve_notes_window(self):
        retrieve_window = tk.Toplevel(self.root)
        retrieve_window.title("Retrieve Notes")

        retrieve_label = tk.Label(retrieve_window, text="Saved Notes:")
        retrieve_label.pack(pady=5)

        retrieve_text = tk.Text(retrieve_window, height=33, width=160)
        retrieve_text.pack(pady=10)

        saved_notes = self.smart_board.retrieve_notes()
        for note in saved_notes:
            retrieve_text.insert(tk.END, note + '\n')

    def save_notes(self, notes_text):
        note_content = notes_text.get("1.0", tk.END)
        self.smart_board.add_note(note_content.strip())
        notes_text.delete("1.0", tk.END)
        self.add_widgets_to_notes_frame()

# Flask thread
def run_flask_app():
    app.run(debug=True)

# Main block
if __name__ == "__main__":
    thread_flask = threading.Thread(target=run_flask_app)
    thread_flask.start()

    root = tk.Tk()
    app = SmartBoardApp(root, smart_board)
    root.geometry("800x600")
    root.mainloop()
