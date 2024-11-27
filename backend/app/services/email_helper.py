import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()  # Memuat variabel lingkungan dari file .env

def send_email(subject, body, recipient_email):
    # Fungsi untuk mengirim email
    smtp_host = "smtp.gmail.com"  # Host SMTP untuk Gmail
    smtp_port = 587  # Port untuk koneksi TLS
    smtp_user = os.getenv("SMTP_USER")  # Mengambil username SMTP dari variabel lingkungan
    smtp_password = os.getenv("SMTP_PASSWORD")  # Mengambil password SMTP dari variabel lingkungan
    from_addr = os.getenv("FROM_ADDR")  # Mengambil alamat email pengirim dari variabel lingkungan

    msg = MIMEMultipart()  # Membuat objek email multipart
    msg["From"] = from_addr  # Menetapkan alamat pengirim
    msg["To"] = recipient_email  # Menetapkan alamat penerima
    msg["Subject"] = subject  # Menetapkan subjek email

    msg.attach(MIMEText(body, "plain"))  # Menambahkan bagian teks ke email

    server = smtplib.SMTP(smtp_host, smtp_port)  # Membuat objek server SMTP
    server.starttls()  # Memulai TLS untuk keamanan
    server.login(smtp_user, smtp_password)  # Masuk ke server SMTP menggunakan kredensial

    server.sendmail(from_addr, recipient_email, msg.as_string())  # Mengirim email
    server.quit()  # Menutup koneksi ke server SMTP
