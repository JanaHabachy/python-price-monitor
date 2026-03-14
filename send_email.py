import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv


def send_email(message):

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")

    receiver = "jana.habachy@icloud.com"

    msg = MIMEText(message)

    msg["Subject"] = "Price Change Alert"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)

    server.send_message(msg)

    server.quit()

    print("Email alert sent!")