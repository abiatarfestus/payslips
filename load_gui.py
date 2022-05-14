from email import message
import os
import sys
import shutil
import split_pdf
import send_email
from PyQt5.uic import loadUi
from pathlib import PurePath
from PyQt5 import QtWidgets
from db import (
    create_connection,
    select_all_employees,
    select_account,
    select_all_messages,
)
from PyQt5.QtWidgets import QDialog, QMainWindow, QPushButton

# from PyQt5.QtGui import QPixmap


parent_dir = None  # Parent Directory path
office = None
month = None
directory = None
path = None  # Path to where new payslip files will be saved


def create_dir():
    """Creates a salary month directory"""
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
            print(f"New directory {directory} created in {parent_dir}")
        except OSError as error:
            print(error)
    return
    # print(os.listdir(path))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        global office
        global month
        global directory
        loadUi("main_window.ui", self)
        office = self.cbx_office.Value
        month = self.cbx_month.Value
        directory = office + "_" + month
        # self.setWindowTitle("Payslips Distributor v1.0")
        self.statusbar.showMessage("Ready")
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 120)
        self.table_widget.setColumnWidth(2, 150)
        self.table_widget.setColumnWidth(3, 120)
        self.table_widget.setColumnWidth(4, 200)
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_start.clicked.connect(self.start_process)
        # self.cancel_button.clicked.connect(self.cancel_process)
        # self.acc_combo.change.set...
        self.btn_update_account.clicked.connect(self.add_update_account)
        self.load_data()

    def load_data(self):
        conn = create_connection("mydb.db")
        rows = select_all_employees(conn)
        # print(f"ROWS: {rows}")
        row = 0
        self.table_widget.setRowCount(len(rows))
        for r in rows:
            # self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(r.rowid))
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(r[2]))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(r[3]))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(r[4]))
            row = row + 1
        # self.table_widget.insertRow(self.table_widget.rowCount())

    def select_file(self):
        self.payslips_file_path = PureWindowsPath(self.lbl_file_path.Text)
        return

    def start_process(self):
        global parent_dir
        global path
        if self.cbx_month.Value != "Choose Month":
            parent_dir = self.payslips_file_path.parents[0]
            path = os.path.join(
                parent_dir, directory
            )  # Path to where new payslip files will be saved

            # =MAKE DIRECTORY=#
            create_dir()
            try:
                # move payslips.pdf file to the new folder
                shutil.move(parent_dir + "\\payslips.pdf", path)
                print(f"payslips.pdf moved to the folder: {directory}")
            except Exception as e:
                print(e)

            # =SPLIT AND EXTRACT PDF=#
            split_pdf.extract_payslips()

            # =SEND EMAIL=#
            self.email = self.cbx_sender.Value
            account = select_account(create_connection, self.email)
            employees = select_all_employees(create_connection)
            _message = select_all_messages(create_connection)
            name = account[0]
            password = account[2]
            _smtp = account[3]
            port = account[4]
            subject = _message[0]
            message = _message[1]
            send_email.email_payslip(
                self.email,
                password,
                employees,
                name=name,
                _smtp=_smtp,
                port=port,
                subject=subject,
                message=message,
            )

            # print("")
            # input("Press Enter to close the program!")

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
