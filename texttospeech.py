import tkinter as tk
from tkinter import Button
import pyttsx3

class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text to Speech App")

        # Text-to-speech components
        self.text_entry = tk.Text(master, width=100, height=25, font=('Arial', 14))
        self.text_entry.pack(pady=10, padx=10)

        self.button_speak = Button(master, text="Speak Aloud", command=self.speak_aloud)
        self.button_speak.pack()

        # Pyttsx3 setup for voice alert
        self.engine = pyttsx3.init()
        self.alert_message = "Your voice is too high. Please keep it down."

    def speak_aloud(self):
        text = self.text_entry.get("1.0", tk.END)  # Get all the text in the Text widget
        if text:
            self.text_to_speech(text)

    def text_to_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)

    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("+{}+{}".format(position_right, position_down))
    root.mainloop()
