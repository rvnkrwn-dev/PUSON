import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, recipient_email):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "2211102010@ittelkom-pwt.ac.id"
    smtp_password = "1700428480@Chiel.yu"
    from_addr = "2211102010@ittelkom-pwt.ac.id"

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    server.sendmail(from_addr, recipient_email, msg.as_string())
    server.quit()
