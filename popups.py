from PyQt5.QtWidgets import QMessageBox


def display_message(message, office=None, month=None, path=None, emails_sent=0, record=None):
    if message == "confirm_process":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Process")
        msg.setText(
            f"You've chosen to process {month} payslips of {office} office in the file: \n{path}"
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_update":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Update")
        msg.setText(
            "This operation will modify the selected database record."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif message == "confirm_delete":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(
            f"This operation will delete {record} from the database."
        )
        msg.setInformativeText("Would you like to proceed?")
        response = msg.exec_()
        return response
    elif type(message) == int:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Finished processing!")
        msg.setInformativeText(f"Total emails successfully sent: {message}")
        msg.exec_()
    elif message == "no_file":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("No file or month is selected for processing!")
        msg.setInformativeText("Please ensure that you've selected both the file with payslips and the pay month.")
        msg.exec_()
    elif message == "success_update":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully updated!")
        msg.exec_()
    elif message == "success_create":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully created!")
        msg.exec_()
    elif message == "success_delete":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Record was successfully deleted!")
        msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Oops! Something went wrong!")
        msg.setDetailedText(message)
        msg.exec_()