import requests
import tkinter as tk
from tkinter import Entry, Button, scrolledtext, Toplevel
import speech_recognition as sr
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pyttsx3

# Flask server URL
FLASK_SERVER_URL = 'http://127.0.0.1:5000'

# Global variable to indicate a high decibel alert
high_decibel_alert = False

def send_alert(message):
    print(f"ALERT: {message}")
    # Open a new window to display the alert message
    alert_window = Toplevel()
    alert_window.title("Alert Window")
    alert_label = tk.Label(alert_window, text=message, font=('Arial', 14))
    alert_label.pack(pady=10)
    # You can customize this window further if needed.

def send_data_to_flask(data):
    try:
        response = requests.post(f'{FLASK_SERVER_URL}/send_data', json=data)
        response.raise_for_status()  # Raise an exception for bad responses
        print(response.json())  # Print the response from the server, if needed
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Flask server: {e}")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def set_high_decibel_alert():
    global high_decibel_alert
    high_decibel_alert = True

class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text to Speech and Speech to Text App")

        # Text-to-speech components
        self.text_entry = Entry(master, width=40, font=('Arial', 12))
        self.text_entry.pack(pady=10, padx=10)

        self.button_speak = Button(master, text="Speak Aloud", command=self.speak_aloud, font=('Arial', 12))
        self.button_speak.pack()

        # Speech-to-text components
        self.text_output = scrolledtext.ScrolledText(master, width=50, height=10, font=('Arial', 12))
        self.text_output.pack(pady=10)

        self.label_decibel = tk.Label(master, text="Decibel Level: ", font=('Arial', 12))
        self.label_decibel.pack()

        self.button_start = Button(master, text="Start Speech to Text", command=self.start_speech_to_text, font=('Arial', 12))
        self.button_start.pack()

        # Pyttsx3 setup for voice alert
        self.engine = pyttsx3.init()
        self.alert_message = "Your voice is too high. Please keep it down."

        # Flag to track if speech-to-text is actively listening
        self.is_listening = False

        # Timer for automatically turning off speech-to-text after a pause
        self.listen_timer = None

        # Thread for continuous speech-to-text listening
        self.listen_thread = threading.Thread(target=self.listen_continuous)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def speak_aloud(self):
        text = self.text_entry.get()
        if text:
            text_to_speech(text)

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
            send_data_to_flask(data)

        except sr.UnknownValueError:
            self.text_output.insert(tk.END, "Could not understand audio\n")
        except sr.RequestError as e:
            self.text_output.insert(tk.END, "Error with the request; {0}\n".format(e))

        # Update decibel level label
        decibel_level = recognizer.energy_threshold
        self.label_decibel.config(text=f"Decibel Level: {decibel_level}")

        # Check decibel level and play alert if too high
        if decibel_level > 4000:  # Adjust this threshold based on your needs
            print("Decibel level too high! Keep your voice low.")
            send_alert("Alert sent to: @tutor,@HOD   Message:High decibel alert in Class-A.")
            self.play_alert_message()

    def play_alert_message(self):
        self.engine.say(self.alert_message)
        self.engine.runAndWait()
        set_high_decibel_alert()

        # Send email using Brevo
        if high_decibel_alert:
            sender_email = "no519989@gmail.com"  # Replace with your email
            recipient_email = "lipekaybps12a1@gmail.com"  # Replace with recipient's email
            subject = "High Decibel Alert"
            body = "High decibel alert in the class. Please take necessary action."

            # Brevo email configuration
            brevo_host = "smtp-relay.brevo.com"
            brevo_port = 587
            brevo_username = "no519989@gmail.com"
            brevo_password = "MUmGXfC10NhsP6c2"

            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Establish a connection to the Brevo SMTP server
            with smtplib.SMTP(brevo_host, brevo_port) as server:
                server.starttls()
                server.login(brevo_username, brevo_password)
                text = message.as_string()
                server.sendmail(sender_email, recipient_email, text)

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
                if decibel_level > 1800:  # Adjust this threshold based on your needs
                    print("Decibel level too high! Keep your voice low.")
                    send_alert("Alert sent to: @tutor,@HOD   Message: High decibel alert in Class-A.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)

    # Adjust the window size for a 5-inch display
    window_width = 480  # Adjust as needed
    window_height = 320  # Adjust as needed
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, position_right, position_down))

    root.mainloop()
