import pyttsx3
import tkinter as tk
from tkinter import Entry, Button, scrolledtext
import speech_recognition as sr
from nexmo import Client as NexmoClient

class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text to Speech and Speech to Text App")

        # Center the text-to-speech components
        self.text_entry = Entry(master, width=50, font=('Arial', 14))
        self.text_entry.pack(pady=10, padx=10)

        self.button_speak = Button(master, text="Speak Aloud", command=self.speak_aloud)
        self.button_speak.pack()

        # Center the speech-to-text components
        self.text_output = scrolledtext.ScrolledText(master, width=60, height=20)
        self.text_output.pack(pady=10)

        self.label_decibel = tk.Label(master, text="Decibel Level: ")
        self.label_decibel.pack()

        self.button_start = Button(master, text="Start Speech to Text", command=self.start_speech_to_text)
        self.button_start.pack()

        # Create a Tkinter Text widget for displaying messages
        self.message_display = scrolledtext.ScrolledText(master, width=60, height=20)
        self.message_display.pack(pady=10)

        # Pyttsx3 setup for voice alert
        self.engine = pyttsx3.init()
        self.alert_message = "Your voice is too high. Please keep it down."

        # Nexmo setup
        self.nexmo_api_key = "40706a57"
        self.nexmo_api_secret = "VCFtAW5997Lov35E"
        self.nexmo_phone_number = "your_nexmo_phone_number"
        self.receiver_phone_number = "+918072339524"  # Your recipient's phone number

        self.nexmo_client = NexmoClient(key=self.nexmo_api_key, secret=self.nexmo_api_secret)

        # Flag to track if speech-to-text is actively listening
        self.is_listening = False

        # Timer for automatically turning off speech-to-text after a pause
        self.listen_timer = None

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
        except sr.UnknownValueError:
            self.text_output.insert(tk.END, "Could not understand audio\n")
        except sr.RequestError as e:
            self.text_output.insert(tk.END, "Error with the request; {0}\n".format(e))

        # Update decibel level label
        decibel_level = recognizer.energy_threshold
        self.label_decibel.config(text=f"Decibel Level: {decibel_level}")

        # Check decibel level and play alert if too high
        if decibel_level > 1100:  # Adjust this threshold based on your needs
            print("Decibel level too high! Keep your voice low.")
            self.play_alert_message()

    def play_alert_message(self):
        self.engine.say(self.alert_message)
        self.engine.runAndWait()

        # Send SMS alert using Nexmo
        self.send_sms_alert("High decibel alert! Keep your voice down.")

    def send_sms_alert(self, message):
        try:
            response = self.nexmo_client.send_message({
                'from': self.nexmo_phone_number,
                'to': self.receiver_phone_number,
                'text': message,
            })

            message_status = response['messages'][0]['status']
            alert_message = f"Nexmo SMS alert sent successfully. Status: {message_status}"
            print(alert_message)  # For debugging in the terminal
            self.message_display.insert(tk.END, alert_message + "\n")

        except Exception as e:
            error_message = f"Error sending Nexmo SMS alert: {str(e)}"
            print(error_message)  # For debugging in the terminal
            self.message_display.insert(tk.END, error_message + "\n")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)

    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)
    root.geometry("+{}+{}".format(position_right, position_down))

    root.mainloop()
