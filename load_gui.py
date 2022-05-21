import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from db import (
    create_connection,
    select_all_employees,
    select_all_accounts,
    create_employee,
    select_employee,
    update_employee
)
from popups import display_message
from worker_thread import Worker
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog

class EmployeeDialog(QDialog):
    def __init__(self, rowid=0, record=None):
        super(EmployeeDialog, self).__init__()
        loadUi("employee_form.ui", self)
        self.rowid = rowid
        if rowid == 0:
            self.lbl_emp_form_heading.setText("Add a New Employee to the Database")
            self.rbtn_create_employee.setChecked(True)
            self.btn_create.setText("Add")
        else:
            self.lbl_emp_form_heading.setText("Update an Employee in the Database")
            self.rbtn_update_employee.setChecked(True)
            self.row_id.setText(str(rowid))
            self.employee_code.setText(record[0])
            self.surname.setText(record[1])
            self.first_name.setText(record[2])
            self.file_name.setText(record[3])
            self.email.setText(record[4])
            self.btn_create.setText("Update")
        self.btn_create.clicked.connect(self.create_update_employee)
        self.btn_cancel.clicked.connect(self.cancel_operation)

    def create_update_employee(self):
        rowid = int(self.row_id.text())
        emp_code = self.employee_code.text()
        surname = self.surname.text()
        first_name = self.first_name.text()
        file_name = self.file_name.text()
        email = self.email.text()
        conn = create_connection('mydb.db')
        if self.rbtn_create_employee.isChecked():
            create_employee(conn, (emp_code, surname, first_name, file_name, email))
        else:
            update_employee(conn, (emp_code, surname, first_name, file_name, email, rowid))

    def cancel_operation(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.office = self.cbx_office.currentText()
        self.month = self.cbx_month.currentText()
        self.payslips_path = None
        self.email = self.cbx_account.currentText()
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
        self.btn_add_new_employee.clicked.connect(self.add_new_employee)
        self.btn_update_employee.clicked.connect(self.update_employee)
        self.btn_update_account.clicked.connect(self.add_update_account)
        self.load_data()

    def load_data(self):
        conn = create_connection("mydb.db")
        rows = select_all_employees(conn)
        accounts = select_all_accounts(conn)
        print(f'Accounts: {accounts}')
        row = 0
        self.table_widget.setRowCount(len(rows))
        for r in rows:
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(r[0]))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(r[1]))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(r[2]))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(r[3]))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(r[4]))
            row = row + 1
        for account in accounts:
            self.cbx_account.addItem(account[1])

    def set_email(self):
        self.email = self.cbx_account.currentText()
        return

    def set_month(self):
        self.month = self.cbx_month.currentText()
        # self.directory = self.office + "_" + self.month
        return

    def set_office(self):
        self.office = self.cbx_office.currentText()
        # self.directory = self.office + "_" + self.month
        return

    def update_statusbar(self, update_message):
        self.statusbar.showMessage(update_message)
        return

    def select_file(self):
        file_name_tuple = QFileDialog.getOpenFileName(
            self, "Open File", "c:\\", "PDF Files (*.pdf)"
        )
        if file_name_tuple:
            self.payslips_path = file_name_tuple[0]
            self.lbl_file_path.setText(self.payslips_path)
        return

    def start_process(self):
        if self.month != "Choose Month" and self.payslips_path != None and self.payslips_path != "":
            if (
                display_message(
                    "confirm_process",
                    office=self.office,
                    month=self.month,
                    path=self.lbl_file_path.text(),
                )
                == QMessageBox.Yes
            ):
                self.parent_dir = os.path.dirname(self.payslips_path)
                # Create a QThread object
                self.thread = QThread()
                # Create a worker object
                self.worker = Worker(month=self.month, office=self.office, payslips_path=self.payslips_path, email=self.email)
                # Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.worker.dir_created.connect(self.update_statusbar)
                self.worker.extracting.connect(self.update_statusbar)
                self.worker.emailing.connect(self.update_statusbar)
                self.worker.int_message.connect(display_message)
                self.worker.str_message.connect(display_message)
                
                # Start the thread
                self.thread.start()
            else:
                pass
        else:
            display_message("no_file")

    def cancel_process(self):
        pass

    def add_new_employee(self):
        self.employee = EmployeeDialog()
        self.employee.show()

    def update_employee(self):
        if self.table_widget.currentRow() != -1:
            current_row = self.table_widget.currentRow()
            print(current_row)
            emp_code_cell = self.table_widget.item(current_row, 0)
            print(current_row, emp_code_cell.text())
            if (emp_code_cell and emp_code_cell.text):
                employee_code = emp_code_cell.text()
                conn = create_connection('mydb.db')
                rowid = select_employee(conn, employee_code)
                record = [self.table_widget.item(current_row, i).text() for i in range(5)]
                self.employee = EmployeeDialog(rowid, record)
                self.employee.show()
            else:
                display_message("The selected row has no employee code.")
        else:
            display_message("No row was selected.")

    
    def add_update_account(self):
        pass