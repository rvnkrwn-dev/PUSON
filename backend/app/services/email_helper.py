import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()


def send_email(subject, body, recipient_email):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_addr = os.getenv("FROM_ADDR")

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    server.sendmail(from_addr, recipient_email, msg.as_string())
    server.quit()
