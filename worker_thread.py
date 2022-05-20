import os
import smtplib
import shutil
from split_pdf import extract_payslips
from popups import display_message
from email.message import EmailMessage
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog
from db import (
    create_connection,
    select_all_employees,
    select_account,
    select_all_messages,
)


class Worker(QObject):
    finished = pyqtSignal()
    dir_created = pyqtSignal(str)
    extracting = pyqtSignal(str)
    emailing = pyqtSignal(str)
    int_message = pyqtSignal(int)
    str_message = pyqtSignal(str)

    def __init__(self, month, office, payslips_path, email):
        super(Worker, self).__init__()
        self.email = email
        self.month = month
        self.office = office
        self.payslips_path = payslips_path
        self.file_name = os.path.basename(self.payslips_path)
        self.directory = (self.office + "_" + self.month)  # Name (Office_Month) of the new folder to be created to hold extracted files
        self.parent_dir = os.path.dirname(self.payslips_path) # Directory where the payslips file is originally located
        self.path = os.path.join(self.parent_dir, self.directory).replace("\\", "/") # Path to where new payslip files will be saved (parent_dir + directory)

    def run(self):
        """Long-running task."""
        if self.create_dir():
            self.extracting.emit('Splitting and extracting PDFs...')
        if extract_payslips(self.path, self.file_name):
            self.extracting.emit('Finished splitting and extracting PDFs!')
            self.email_payslip()
        self.finished.emit()
        

    def create_dir(self):
        """Creates a salary month directory"""
        if not os.path.isdir(self.path):
            try:
                os.mkdir(self.path)
                self.dir_created.emit(f"New directory {self.directory} created in {self.parent_dir}")
            except Exception as e:
                self.str_message.emit(repr(e))
                return False
        try:
            shutil.move(
                os.path.join(self.parent_dir, self.file_name), self.path
            )
            self.dir_created.emit(f"{self.file_name} moved to the folder: {self.directory}")
            return True
        except Exception as e:
            self.str_message.emit(repr(e))
            return False


    def email_payslip(self):
        '''Email payslips in the path directory to corresponding emails'''
        try:
            conn = create_connection("mydb.db")
            account = select_account(conn, self.email)
            employees = select_all_employees(conn)
            _message = select_all_messages(conn)
            account_name = account[0]
            self.email = account[1]
            password = account[2]
            _smtp = account[3]
            port = account[4]
            message = _message[1]
            emails_sent = 0
            files = os.listdir(self.path)
            employee_dict = {employee[3]: employee[4] for employee in employees}
            for file in files:
                print(f'Current file: {file}')
                # if file in employee_dict.keys():
                if file in ['Abiatar.pdf', 'AbiatarFU.pdf']:
                    msg = EmailMessage()
                    msg["Subject"] = f"{self.month} Payslip"
                    msg["From"] = self.email
                    msg["To"] = employee_dict[file]
                    receiver = file[:-4]
                    msg.set_content(message.format(sender=account_name, receiver=receiver, month=self.month))
                    # print(f'Recipient: {msg["To"]}')
                    with open(os.path.join(self.path, file), "rb") as f:
                        file_data = f.read()
                    msg.add_attachment(
                        file_data, maintype="application", subtype="octet-stream", filename=file
                    )
                    with smtplib.SMTP_SSL(_smtp, port) as smtp:
                        # print(email, password, _smtp, port, )
                        try:
                            smtp.login(self.email, password)
                            smtp.send_message(msg)
                            self.emailing.emit(f'Emailing {file} to {employee_dict[file]}...')
                            emails_sent += 1
                        except Exception as e:
                            self.str_message.emit(repr(e))
            self.emailing.emit('Emailing complete!')
            self.int_message.emit(emails_sent)
        except Exception as e:
            self.str_message.emit(repr(e))
        return