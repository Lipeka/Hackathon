import sounddevice as sd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from soundmeter import SoundMeter

# Set the threshold for sound level in decibels
threshold_db = 70  # Adjust this value based on your requirements

# Set the email credentials
email_sender = "admin@gmail.com"
email_receiver = "727722euai031@skcet.ac.in"
email_password = "your_email_password"

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

def check_sound_level(indata, frames, time, status):
    # Calculate the root mean square (RMS) of the sound level
    rms = np.sqrt(np.mean(indata**2))
    
    # Convert RMS to decibels
    rms_db = 20 * np.log10(rms)

    # Check if the sound level is above the threshold in decibels
    if rms_db > threshold_db:
        print(f"Sound level: {rms_db:.2f} dB. Reduce your volume!")

        # Send an email alert
        subject = "High Sound Alert"
        message = f"The sound level is too high ({rms_db:.2f} dB). Please reduce your volume."
        send_email(subject, message)

# Set up the audio stream
duration = 10  # Set the duration for capturing sound (in seconds)
sample_rate = 44100  # Set the sample rate
sd.default.samplerate = sample_rate
sd.default.channels = 1  # Mono audio input

# Start the audio stream with the callback function
with sd.InputStream(callback=check_sound_level):
    sd.sleep(duration * 1000)
