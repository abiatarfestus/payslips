import os
import json
import smtplib
from load_gui import path, month
from email.message import EmailMessage

# email = email
# password = password
# employees = employees


def email_payslip(email, password, employees, _smtp, port, subject, message):
    emails_sent = 0
    files = os.listdir(path)
    employee_dict = {employee[3]: employee[4] for employee in employees}
    for file in files:
        print(f"Current file: {file}")
        if file in employee_dict.keys():
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = email
            msg["To"] = employee_dict[file]
            msg.set_content(message)
            with open(os.path.join(path, file), "rb") as f:
                file_data = f.read()
            msg.add_attachment(
                file_data, maintype="application", subtype="octet-stream", filename=file
            )
            with smtplib.SMTP_SSL(_smtp, port) as smtp:
                try:
                    smtp.login(email, password)
                    smtp.send_message(msg)
                    print("Sending email...")
                    emails_sent += 1
                except Exception as e:
                    print(e)
    print(f"Successfully sent {emails_sent} emails!")
    return
