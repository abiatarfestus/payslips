import os
import smtplib
from email.message import EmailMessage


def email_payslip(email, password, employees, path, sender, _smtp, port, month, message):
    emails_sent = 0
    files = os.listdir(path)
    employee_dict = {employee[3]: employee[4] for employee in employees}
    for file in files:
        # if file in employee_dict.keys():
        if file in ['Abiatar.pdf', 'AbiatarFU.pdf']:
            msg = EmailMessage()
            msg["Subject"] = f"{month} Payslip"
            msg["From"] = email
            msg["To"] = employee_dict[file]
            receiver = file[:-4]
            msg.set_content(message.format(sender=sender, receiver=receiver, month=month))
            print(message.format(sender=sender, receiver=receiver, month=month))
            with open(os.path.join(path, file), "rb") as f:
                file_data = f.read()
            msg.add_attachment(
                file_data, maintype="application", subtype="octet-stream", filename=file
            )
            with smtplib.SMTP_SSL(_smtp, port) as smtp:
                print(email, password, _smtp, port, )
                try:
                    smtp.login(email, password)
                    smtp.send_message(msg)
                    print("Sending email...")
                    emails_sent += 1
                except Exception as e:
                    print(e)
    print(f"Successfully sent {emails_sent} emails!")
    return
