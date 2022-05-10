import os
import json
from env import *
import smtplib
from make_dir import path, directory, month
from email.message import EmailMessage

EMAIL_ADDRESS = EMAIL_ADDRESS
EMAIL_PASSWORD = EMAIL_PASSWORD
staffs = STAFFS


def email_payslip():
    emails_sent = 0
    files = os.listdir(path)
    for file in files:
        print(f'Current file: {file}')
        if  file in staffs.keys():
            msg = EmailMessage()
            msg['Subject'] = 'Payslip'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = staffs[file]
            msg.set_content(f'Good day!\n\nAttached please find your payslip of {month} as received from Salary.\nNB: Please take note that the process to extract your payslip from others and email it to you was done with an automated program. Thus, if you received a wrong payslip, do let me know so I fix it, and I do apologise for that.\n\nRegards,\nShingenge')
            print(f'Recipient: {msg["To"]}')
            with open(os.path.join(path, file),'rb') as f:
                file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                try:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                    print('Sending email...')
                    emails_sent +=1
                except Exception as e:
                    print(e)
    print(f'Successfully sent {emails_sent} emails!')
    return