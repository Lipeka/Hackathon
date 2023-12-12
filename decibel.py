import pyaudio
import numpy as np
import smtplib
from email.mime.text import MIMEText
import pyttsx3
import time
# Set the threshold for sound level in decibels
threshold_db = 70  # Adjust this value based on your requirements
silence_duration = 180  # Duration of silence to stop recording (in seconds)
prompt_duration = 5  # Duration of prompt for user to speak (in seconds)
# Set the email credentials
email_sender = "admin@gmail.com"
email_receiver = "727722euai031@skcet.ac.in"
email_password = "your_email_password"
# Set up text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()
def send_email(subject, message):
    try:
        # Set up the email server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        # Log in to your email account
        server.login(email_sender, email_password)
        # Compose the email
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = email_sender
        msg['To'] = email_receiver
        # Send the email
        server.sendmail(email_sender, email_receiver, msg.as_string())
        # Close the server connection
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
def check_sound_level(in_data, frame_count, time_info, status):
    global silence_counter, recording
    # Convert raw byte data to NumPy array
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    # Calculate the root mean square (RMS) of the sound level
    rms = np.sqrt(np.mean(audio_data**2))
    # Convert RMS to decibels
    rms_db = 20 * np.log10(rms)
    # Check if the sound level is above the threshold in decibels
    if rms_db > threshold_db:
        print(f"Sound level: {rms_db:.2f} dB. Reduce your volume!")
        # Send an email alert
        subject = "High Sound Alert"
        message = f"The sound level is too high ({rms_db:.2f} dB). Please reduce your volume."
        send_email(subject, message)
        # Speak the alert message
        speak("Warning! The sound level is too high. Please reduce your volume.")
    # Check for silence to stop/start recording
    if rms_db <= threshold_db:
        silence_counter += 1
        if silence_counter >= silence_duration * (sample_rate // chunk_size):
            if recording:
                print("Recording stopped due to silence.")
                recording = False
                stop_recording()
        elif not recording:
            print("Recording started.")
            recording = True
            start_recording()
    else:
        silence_counter = 0
def start_recording():
    global stream
    # Start the audio stream with the callback function
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size,
                    stream_callback=check_sound_level)
def stop_recording():
    global stream
    # Stop the audio stream
    stream.stop_stream()
    stream.close()
# Set up the audio stream
sample_rate = 44100  # Set the sample rate
chunk_size = 1024  # Adjust the chunk size based on your requirements
recording = False  # Flag to indicate whether recording is active
silence_counter = 0  # Counter for tracking silence
# Initialize PyAudio
p = pyaudio.PyAudio()
# Start the audio stream
start_recording()
print("Recording...")
try:
    while True:
        if recording:
            # Prompt the user to speak
            speak("Please speak now.")
            time.sleep(1)  # or time.sleep(1)
        else:
            # Sleep when not recording to conserve resources
            time.sleep(1)  # or time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # Cleanup resources
    if recording:
        stop_recording()
    p.terminate()
print("Recording stopped.")
