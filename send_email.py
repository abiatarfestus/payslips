import os
import smtplib
from popups import display_message
from email.message import EmailMessage
from PyQt5.QtWidgets import QMessageBox


def email_payslip(email, password, employees, path, sender, _smtp, port, month, message):
    try:
        emails_sent = 0
        files = os.listdir(path)
        employee_dict = {employee[3]: employee[4] for employee in employees}
        for file in files:
            print(f'Current file: {file}')
            # if file in employee_dict.keys():
            if file in ['Abiatar.pdf', 'AbiatarFU.pdf']:
                msg = EmailMessage()
                msg["Subject"] = f"{month} Payslip"
                msg["From"] = email
                msg["To"] = employee_dict[file]
                receiver = file[:-4]
                msg.set_content(message.format(sender=sender, receiver=receiver, month=month))
                print(f'Recipient: {msg["To"]}')
                with open(os.path.join(path, file), "rb") as f:
                    file_data = f.read()
                msg.add_attachment(
                    file_data, maintype="application", subtype="octet-stream", filename=file
                )
                with smtplib.SMTP_SSL(_smtp, port) as smtp:
                    # print(email, password, _smtp, port, )
                    try:
                        smtp.login(email, password)
                        smtp.send_message(msg)
                        print("Sending email...")
                        emails_sent += 1
                    except Exception as e:
                        display_message(repr(e))
        display_message("process_done", emails_sent=emails_sent)
    except Exception as e:
        display_message(repr(e))
    return