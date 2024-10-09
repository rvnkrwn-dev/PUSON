import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, recipient_email):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "2211102010@ittelkom-pwt.ac.id"
    smtp_password = "??????????"
    from_addr = "2211102010@ittelkom-pwt.ac.id"

    # Membuat objek MIMEMultipart
    msg = MIMEMultipart()
    msg["From"] = "puson.support"
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Menambahkan body ke email
    msg.attach(MIMEText(body, "plain"))

    # Membuat koneksi ke server SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    # Mengirim email
    server.sendmail(from_addr, recipient_email, msg.as_string())
    server.quit()
