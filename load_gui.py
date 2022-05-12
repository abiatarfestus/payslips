import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from db import create_connection, select_all_employees
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 120)
        self.table_widget.setColumnWidth(2, 150)
        self.table_widget.setColumnWidth(3, 120)
        self.table_widget.setColumnWidth(4, 200)
        self.select_file_button.clicked.connect(self.select_file)
        self.start_button.clicked.connect(self.start_process)
        self.cancel_button.clicked.connect(self.cancel_process)
        # self.acc_combo.change.set...
        self.update_acc_button.clicked.connect(self.add_update_account)
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

    def select_file(self):
        pass

    def start_process(self):
        pass

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
