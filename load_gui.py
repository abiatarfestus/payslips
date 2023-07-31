import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from db import (
    setup_db,
    create_connection,
    select_all_employees,
    select_all_accounts,
    select_all_offices,
    create_employee,
    create_account,
    create_office,
    create_message,
    select_employee,
    select_account,
    select_office,
    select_message,
    update_employee,
    update_account,
    update_office,
    update_message,
    delete_employee,
)
from popups import display_message
from worker_thread import Worker
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog


def initialise_db():
    setup_db()
    conn = create_connection("mydb.db")
    record = select_message(conn)
    if record == None:
        new_message = (
            "Good day, {receiver}!\n\nAttached please find your payslip of {month} as received from Salary.\nNB: Please take note that the process to extract your payslip from others and email it to you was done with an automated program. Thus, if you received a wrong payslip, do let me know so I fix it, and I do apologise for that.\n\nRegards,\n\n{sender}",
        )
        create_message(conn, new_message)
    return


class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()
        loadUi("about.ui", self)
        self.setWindowTitle("About")


class MessageDialog(QDialog):
    def __init__(self, rowid, message):
        super(MessageDialog, self).__init__()
        loadUi("message_editor.ui", self)
        self.setWindowTitle("Message Editor")
        self.row_id = rowid
        self.message_editor.setPlainText(message)
        self.btn_save.clicked.connect(self.save_message)
        self.btn_cancel.clicked.connect(self.close)

    def save_message(self):
        conn = create_connection("mydb.db")
        message = self.message_editor.toPlainText().strip()
        update_message(conn, (message, self.row_id))
        self.close()
        return


class OfficeDialog(QDialog):
    office_updated = pyqtSignal()

    def __init__(self, rowid=0, record=None):
        super(OfficeDialog, self).__init__()
        loadUi("office_form.ui", self)
        self.setWindowTitle("Office Form")
        self.rowid = rowid
        self.row_id.setEnabled(False)
        if rowid == 0:
            self.lbl_office_form_heading.setText("Add a New Office to the Database")
            self.rbtn_create_office.setChecked(True)
            self.btn_create.setText("Add")
        else:
            self.lbl_office_form_heading.setText("Update an Office in the Database")
            self.rbtn_update_office.setChecked(True)
            self.row_id.setText(str(rowid))
            self.office_name.setText(record[1])
            self.btn_create.setText("Update")
        self.btn_create.clicked.connect(self.create_update_office)
        self.btn_cancel.clicked.connect(self.close)
        self.rbtn_create_office.toggled.connect(self.force_create)

    def create_update_office(self):
        office_name = self.office_name.text().strip()
        conn = create_connection("mydb.db")
        if self.rbtn_create_office.isChecked():
            if create_office(conn, (office_name,)):
                self.reset()
        else:
            rowid = int(self.row_id.text())
            if display_message("confirm_update") == QMessageBox.Yes:
                if update_office(conn, (office_name, rowid)):
                    self.rbtn_create_office.setChecked(True)
        self.office_updated.emit()
        return

    def reset(self):
        self.office_name.setText("")
        self.row_id.setText("")
        self.btn_create.setText("Add")
        self.lbl_office_form_heading.setText("Add a New Office to the Database")

    def force_create(self):
        self.reset()
        self.rbtn_update_office.setCheckable(False)


class AccountDialog(QDialog):
    account_updated = pyqtSignal()

    def __init__(self, rowid=0, record=None):
        super(AccountDialog, self).__init__()
        loadUi("account_form.ui", self)
        self.setWindowTitle("Account Form")
        self.rowid = rowid
        self.row_id.setEnabled(False)
        if rowid == 0:
            self.lbl_acc_form_heading.setText("Add a New Email Account to the Database")
            self.rbtn_create_account.setChecked(True)
            self.btn_create.setText("Add")
        else:
            self.lbl_acc_form_heading.setText("Update an Email Account in the Database")
            self.rbtn_update_account.setChecked(True)
            self.row_id.setText(str(rowid))
            self.account_name.setText(record[1])
            self.email.setText(record[2])
            self.password.setText(record[3])
            self.smtp.setText(record[4])
            self.port.setText(str(record[5]))
            self.btn_create.setText("Update")
        self.btn_create.clicked.connect(self.create_update_account)
        self.btn_cancel.clicked.connect(self.close)
        self.rbtn_create_account.toggled.connect(self.force_create)

    def create_update_account(self):
        account_name = self.account_name.text().strip().title()
        email = self.email.text().strip()
        password = self.password.text()
        smtp = self.smtp.text().strip()
        port = self.port.text().strip()
        conn = create_connection("mydb.db")
        if self.rbtn_create_account.isChecked():
            if create_account(conn, (account_name, email, password, smtp, port)):
                self.reset()
        else:
            rowid = int(self.row_id.text())
            if display_message("confirm_update") == QMessageBox.Yes:
                if update_account(
                    conn, (account_name, email, password, smtp, port, rowid)
                ):
                    self.rbtn_create_account.setChecked(True)
        self.account_updated.emit()
        return

    def reset(self):
        self.account_name.setText("")
        self.email.setText("")
        self.password.setText("")
        self.smtp.setText("")
        self.port.setText("")
        self.row_id.setText("")
        self.btn_create.setText("Add")
        self.lbl_acc_form_heading.setText("Add a New Email Account to the Database")

    def force_create(self):
        self.reset()
        self.rbtn_update_account.setCheckable(False)


class EmployeeDialog(QDialog):
    employee_updated = pyqtSignal()

    def __init__(self, rowid=0, record=None):
        super(EmployeeDialog, self).__init__()
        loadUi("employee_form.ui", self)
        self.setWindowTitle("Employee Form")
        self.rowid = rowid
        if rowid == 0:
            self.lbl_emp_form_heading.setText("Add a New Employee to the Database")
            self.rbtn_create_employee.setChecked(True)
            self.rbtn_update_employee.setCheckable(False)
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
        self.btn_cancel.clicked.connect(self.close)

    def create_update_employee(self):
        emp_code = self.employee_code.text().strip().capitalize()
        surname = self.surname.text().strip().title()
        first_name = self.first_name.text().strip().title()
        file_name = self.file_name.text().strip().capitalize()
        email = self.email.text().strip()
        conn = create_connection("mydb.db")
        if self.rbtn_create_employee.isChecked():
            if create_employee(conn, (emp_code, surname, first_name, file_name, email)):
                self.employee_code.setText("")
                self.surname.setText("")
                self.first_name.setText("")
                self.file_name.setText("")
                self.email.setText("")
        else:
            rowid = int(self.row_id.text())
            if display_message("confirm_update") == QMessageBox.Yes:
                if update_employee(
                    conn, (emp_code, surname, first_name, file_name, email, rowid)
                ):
                    self.close()
            else:
                return
        self.employee_updated.emit()
        return


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        initialise_db()
        loadUi("main_window.ui", self)
        self.office = self.cbx_office.currentText()
        self.month = self.cbx_month.currentText()
        self.payslips_path = None
        self.email = self.cbx_account.currentText()
        self.statusbar.showMessage("Ready")
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setColumnWidth(1, 120)
        self.table_widget.setColumnWidth(2, 150)
        self.table_widget.setColumnWidth(3, 120)
        self.table_widget.setColumnWidth(4, 300)
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_delete.clicked.connect(self.delete_employee)
        self.cbx_account.currentIndexChanged.connect(self.set_email)
        self.cbx_month.currentIndexChanged.connect(self.set_month)
        self.cbx_office.currentIndexChanged.connect(self.set_office)
        self.btn_add_new_employee.clicked.connect(self.add_new_employee)
        self.btn_update_employee.clicked.connect(self.update_employee)
        self.btn_update_account.clicked.connect(self.add_update_account)
        self.btn_update_office.clicked.connect(self.add_update_office)
        self.file_open.triggered.connect(self.select_file)
        self.file_edit_message.triggered.connect(self.update_message)
        self.file_add_employee.triggered.connect(self.add_new_employee)
        self.file_add_account.triggered.connect(self.add_update_account)
        self.file_add_office.triggered.connect(self.add_update_office)
        self.help_about.triggered.connect(self.view_about)
        self.file_exit.triggered.connect(QCoreApplication.instance().quit)
        self.load_employees()
        self.load_offices()
        self.load_accounts()

    def load_employees(self):
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

    def load_accounts(self):
        conn = create_connection("mydb.db")
        accounts = select_all_accounts(conn)
        self.cbx_account.clear()
        for account in accounts:
            self.cbx_account.addItem(account[1])

    def load_offices(self):
        conn = create_connection("mydb.db")
        offices = select_all_offices(conn)
        self.cbx_office.clear()
        for office in offices:
            self.cbx_office.addItem(office[0])

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

    def reset_status(self):
        self.statusbar.showMessage("Ready")
        self.lbl_file_path.setText("No File Selected")
        return

    def start_process(self):
        if (
            self.month != "Choose Month"
            and self.payslips_path != None
            and self.payslips_path != ""
            and self.office != ""
        ):
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
                self.worker = Worker(
                    month=self.month,
                    office=self.office,
                    payslips_path=self.payslips_path,
                    email=self.email,
                )
                # Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.reset_status)
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

    def add_new_employee(self):
        self.employee = EmployeeDialog()
        self.employee.employee_updated.connect(self.load_employees)
        self.employee.show()

    def update_employee(self):
        if self.table_widget.currentRow() != -1:
            current_row = self.table_widget.currentRow()
            emp_code_cell = self.table_widget.item(current_row, 0)
            if emp_code_cell and emp_code_cell.text:
                employee_code = emp_code_cell.text()
                conn = create_connection("mydb.db")
                rowid = select_employee(conn, employee_code)
                record = [
                    self.table_widget.item(current_row, i).text() for i in range(5)
                ]
                self.employee = EmployeeDialog(rowid, record)
                self.employee.employee_updated.connect(self.load_employees)
                self.employee.show()
            else:
                display_message("The selected row has no employee code.")
        else:
            display_message("No row was selected.")

    def add_update_account(self):
        conn = create_connection("mydb.db")
        record = select_account(conn, self.email)
        if record == None:
            rowid = 0
        else:
            rowid = record[0]
        self.account = AccountDialog(rowid, record)
        self.account.account_updated.connect(self.load_accounts)
        self.account.show()

    def add_update_office(self):
        conn = create_connection("mydb.db")
        record = select_office(conn, self.office)
        if record == None:
            rowid = 0
        else:
            rowid = record[0]
        self.office_dialog = OfficeDialog(rowid, record)
        self.office_dialog.office_updated.connect(self.load_offices)
        self.office_dialog.show()

    def update_message(self):
        conn = create_connection("mydb.db")
        record = select_message(conn)
        rowid = record[0]
        message = record[1]
        self.message_dialog = MessageDialog(rowid, message)
        self.message_dialog.show()

    def view_about(self):
        self.about_dialog = AboutDialog()
        self.about_dialog.show()

    def delete_employee(self, employee_code):
        if self.table_widget.currentRow() != -1:
            current_row = self.table_widget.currentRow()
            emp_code_cell = self.table_widget.item(current_row, 0)
            record_owner = f"{self.table_widget.item(current_row, 1).text()} {self.table_widget.item(current_row, 2).text()}"
            if emp_code_cell and emp_code_cell.text:
                employee_code = emp_code_cell.text()
                if (
                    display_message("confirm_delete", record=record_owner)
                    == QMessageBox.Yes
                ):
                    conn = create_connection("mydb.db")
                    delete_employee(conn, employee_code)
                    self.load_employees()
            else:
                display_message("The selected row has no employee code.")
        else:
            display_message("No row was selected.")
