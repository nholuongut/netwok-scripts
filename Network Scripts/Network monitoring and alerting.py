import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

def send_email(message):
    sender = "sender@example.com"
    recipient = "recipient@example.com"
    msg = MIMEText(message)
    msg['Subject'] = 'Network Alert'
    msg['From'] = sender
    msg['To'] = recipient
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "your_username"
    smtp_password = "your_password"
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)
    smtp_connection.sendmail(sender, recipient, msg.as_string())
    smtp_connection.quit()

def ping(host):
    response = subprocess.Popen(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = response.communicate()
    return response.returncode

if __name__ == '__main__':
    host = 'google.com'
    while True:
        ping_response = ping(host)
        if ping_response != 0:
            message = f"Ping failed for {host} at {datetime.now()}"
            send_email(message)
        time.sleep(60) # Wait 60 seconds before pinging again