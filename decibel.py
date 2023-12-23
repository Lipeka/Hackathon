import tkinter as tk
from tkinter import scrolledtext, Button, Toplevel
import threading
import speech_recognition as sr
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pyttsx3
import time

# Flask server URL
FLASK_SERVER_URL = 'http://127.0.0.1:5000'

# Global variable to indicate a high decibel alert
high_decibel_alert = False

# Initialize the text-to-speech engine
engine = pyttsx3.init()

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech to Text App")

        # Speech-to-text components
        self.text_output = scrolledtext.ScrolledText(master, width=60, height=20)
        self.text_output.pack(pady=10)

        self.label_decibel = tk.Label(master, text="Decibel Level: ")
        self.label_decibel.pack()

        self.button_start = Button(master, text="Start Speech to Text", command=self.start_speech_to_text)
        self.button_start.pack()

        # Flag to track if speech-to-text is actively listening
        self.is_listening = False

        # Timer for automatically turning off speech-to-text after a pause
        self.listen_timer = None

        # Thread for continuous speech-to-text listening
        self.listen_thread = threading.Thread(target=self.listen_continuous)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        # Timer for the initial alert after 10 seconds
        self.initial_alert_timer = threading.Timer(10, self.initial_alert)
        self.initial_alert_timer.start()

    def initial_alert(self):
        message = "Your voice is too loud. Please keep it down. Mail alert sent"
        print(f"ALERT: {message}")
        # Open a new window to display the alert message
        alert_window = Toplevel()
        alert_window.title("Alert Window")
        alert_label = tk.Label(alert_window, text=message, font=('Arial', 16))
        alert_label.pack(pady=20)

        # Speak the alert message
        engine.say(message)
        engine.runAndWait()

        # Send email for the initial alert
        self.play_alert_message(message)

    def start_speech_to_text(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            self.text_output.insert(tk.END, "You said: " + text + "\n")

            # Send data to Flask server
            data = {'message': text}
            self.send_data_to_flask(data)

        except sr.UnknownValueError:
            self.text_output.insert(tk.END, "Could not understand audio\n")
        except sr.RequestError as e:
            self.text_output.insert(tk.END, f"Error with the request; {e}\n")

        # Update decibel level label
        decibel_level = recognizer.energy_threshold
        self.label_decibel.config(text=f"Decibel Level: {decibel_level}")

        # Check decibel level and play alert if too high
        if decibel_level > 1000:  # Adjust this threshold based on your needs
            print("Decibel level too high! Keep your voice low.")
            self.send_alert("Alert sent to: @tutor,@HOD   Message: High decibel alert in Class-A.")
            self.play_alert_message()

    def play_alert_message(self, message):
        self.set_high_decibel_alert()

        # Send email using Brevo
        if high_decibel_alert:
            sender_email = "lipekadhamodharan@gmail.com"  # Replace with your email
            recipient_email = "no519989@gmail.com"  # Replace with recipient's email
            subject = "High Decibel Alert"
            body = message  # Set the email body to the alert message

            # Brevo email configuration
            brevo_host = "smtp-relay.brevo.com"
            brevo_port = 587
            brevo_username = "lipekadhamodharan@gmail.com"
            brevo_password = "Fk90ad1msbpg8HP6"

            # Create message
            email_message = MIMEMultipart()
            email_message["From"] = sender_email
            email_message["To"] = recipient_email
            email_message["Subject"] = subject
            email_message.attach(MIMEText(body, "plain"))

            # Establish a connection to the Brevo SMTP server
            try:
                with smtplib.SMTP(brevo_host, brevo_port) as server:
                    server.starttls()
                    server.login(brevo_username, brevo_password)
                    text = email_message.as_string()
                    server.sendmail(sender_email, recipient_email, text)
                    print("Email sent successfully.")
            except Exception as e:
                print(f"Error sending email: {e}")

    def set_high_decibel_alert(self):
        global high_decibel_alert
        high_decibel_alert = True

    def send_alert(self, message):
        print(f"ALERT: {message}")
        # Open a new window to display the alert message
        alert_window = Toplevel()
        alert_window.title("Alert Window")
        alert_label = tk.Label(alert_window, text=message, font=('Arial', 16))
        alert_label.pack(pady=20)

        # Speak the alert message
        engine.say("Your voice is too loud. Please keep it down.")
        engine.runAndWait()

        # Send email for the alert
        self.play_alert_message(message)

    def send_data_to_flask(self, data):
        try:
            response = requests.post(f'{FLASK_SERVER_URL}/send_data', json=data)
            response.raise_for_status()  # Raise an exception for bad responses
            print(response.json())  # Print the response from the server, if needed
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to Flask server: {e}")

    def listen_continuous(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening for any voice:")
            while True:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                try:
                    text = recognizer.recognize_google(audio)
                    self.text_output.insert(tk.END, "You said: " + text + "\n")
                except sr.UnknownValueError:
                    pass  # Ignore unknown value errors
                except sr.RequestError as e:
                    print(f"Error with the request: {e}")

                # Update decibel level label
                decibel_level = recognizer.energy_threshold
                self.label_decibel.config(text=f"Decibel Level: {decibel_level}")

                # Check decibel level and play alert if too high
                if decibel_level > 1000:  # Adjust this threshold based on your needs
                    print("Decibel level too high! Keep your voice low.")
                    self.send_alert("Alert sent to: @tutor,@HOD   Message: High decibel alert in Class-A.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)

    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("+{}+{}".format(position_right, position_down))
    root.mainloop()

