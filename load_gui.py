import os
import shutil
import split_pdf
import send_email
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from db import (
    create_connection,
    select_all_employees,
    select_account,
    select_all_messages,
)
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.office = self.cbx_office.currentText()
        self.month = self.cbx_month.currentText()
        self.directory = self.office + "_" + self.month # Name (Office_Month) of the new folder to be created to hold extracted files
        self.path = None # Path to where new payslip files will be saved (parent_dir + directory)
        self.parent_dir = None # Directory where the payslips file is originally located
        self.email = self.cbx_account.currentText()
        self.payslips_path = None  # Absolute path of the payslips.pdf file
        self.statusbar.showMessage("Ready")
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 120)
        self.table_widget.setColumnWidth(2, 150)
        self.table_widget.setColumnWidth(3, 120)
        self.table_widget.setColumnWidth(4, 200)
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_start.clicked.connect(self.start_process)
        self.cbx_account.currentIndexChanged.connect(self.set_email)
        self.cbx_month.currentIndexChanged.connect(self.set_month)
        self.cbx_office.currentIndexChanged.connect(self.set_office)
        self.btn_update_account.clicked.connect(self.add_update_account)
        self.load_data()

    def create_dir(self):
        """Creates a salary month directory"""
        if not os.path.isdir(self.path):
            try:
                os.mkdir(self.path)
                print(f"New directory {self.directory} created in {self.parent_dir}")
            except OSError as error:
                print(error)
        return


    def set_email(self):
        self.email = self.cbx_sender.currentText()
        return

    def set_month(self):
        self.month = self.cbx_month.currentText()
        self.directory = self.office + "_" + self.month
        return

    def set_office(self):
        self.office = self.cbx_office.currentText()
        self.directory = self.office + "_" + self.month
        return

    def load_data(self):
        conn = create_connection("mydb.db")
        rows = select_all_employees(conn)
        row = 0
        self.table_widget.setRowCount(len(rows))
        for r in rows:
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(r[2]))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(r[3]))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(r[4]))
            row = row + 1

    def select_file(self):
        file_name_tuple = QFileDialog.getOpenFileName(
            self, "Open File", "c:\\", "PDF Files (*.pdf)"
        )
        if file_name_tuple:
            self.payslips_path = file_name_tuple[0]
            self.lbl_file_path.setText(self.payslips_path)
        return

    def start_process(self):
        if self.month != "Choose Month" and self.payslips_path != None:
            if self.display_message("confirm_process") == QMessageBox.Yes:
                self.parent_dir = os.path.dirname(self.payslips_path)
                self.file_name = os.path.basename(self.payslips_path)
                self.path = os.path.join(
                    self.parent_dir, self.directory
                )
                self.path = self.path.replace('\\','/')

                # =MAKE DIRECTORY=#
                self.create_dir()
                try:
                    shutil.move(os.path.join(self.parent_dir, self.file_name), self.path)
                    print(f"{self.file_name} moved to the folder: {self.directory}")
                except Exception as e:
                    print(e)

                # =SPLIT AND EXTRACT PDF=#
                split_pdf.extract_payslips(self.path, self.file_name)

                # =SEND EMAIL=#
                conn = create_connection('mydb.db')
                account = select_account(conn, self.email)
                employees = select_all_employees(conn)
                _message = select_all_messages(conn)
                name = account[0]
                self.email = account[1]
                password = account[2]
                _smtp = account[3]
                port = account[4]
                message = _message[1]
                send_email.email_payslip(
                    self.email,
                    password,
                    employees,
                    self.path,
                    sender=name,
                    _smtp=_smtp,
                    port=port,
                    month=self.month,
                    message=message,
                )

                self.display_message("process_done")
            else:
                pass
        else:
            self.display_message("no_file")

    def display_message(self, type):
        if type == "confirm_process":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setWindowTitle("Confirm Process")
            msg.setText(
                f"You've chosen to process payslips of {self.office} for {self.month} in the file: \n{self.lbl_file_path.text()}"
            )
            msg.setInformativeText("Would you like to proceed?")
            response = msg.exec_()
            return response
        elif type == "process_done":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Confirmation")
            msg.setText("Finished processing!")
            msg.setInformativeText(f"A total of {100} emails were successfully sent.")
            response = msg.exec_()
        elif type == "no_file":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No file or month is selected for processing!")
            msg.setInformativeText("Please ensure that you've selected both the file with payslips and the pay month.")
            response = msg.exec_()

    def cancel_process(self):
        pass

    def add_update_account(self):
        pass


# class ChooseMonthDialog(QDialog):
#     def __init__(self):
#         super(ChooseMonthDialog, self).__init__()
#         loadUi("choose_month.ui",self)

#     def loginfunction(self):
#         user = self.emailfield.text()
#         password = self.passwordfield.text()
