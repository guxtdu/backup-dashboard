#!/usr/bin/env python3
import os
import mysql.connector
import smtplib
from email.message import EmailMessage
from datetime import date
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM")

REPORT_DIR = "uploads"
TODAY = date.today().strftime("%Y-%m-%d")

def send_report(to_email, customer):
    html_path = os.path.join(REPORT_DIR, customer, f"report_{TODAY}.html")
    if not os.path.exists(html_path):
        print(f"[⚠] Kein Report für {customer} ({to_email}) gefunden.")
        return

    with open(html_path, "r") as f:
        html = f.read()

    msg = EmailMessage()
    msg["Subject"] = f"Backup-Report {TODAY} – {customer}"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.set_content("Ihr täglicher Backup-Report ist angehängt.")
    msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
            print(f"[✓] E-Mail an {to_email} gesendet.")
    except Exception as e:
        print(f"[❌] Fehler beim Senden an {to_email}: {e}")

def main():
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT customer, email FROM allowed_ips WHERE email_enabled = 1 AND email IS NOT NULL")
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for row in rows:
        send_report(row["email"], row["customer"])

if __name__ == "__main__":
    main()
