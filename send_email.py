import smtplib
from email.mime.text import MIMEText


def send_email(message):

    sender = "jana.habachy@gmail.com"
    password = "bwqmjkmefxzarvme"

    receiver = "aya.habachi02@gmail.com"

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