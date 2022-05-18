from PyQt5.QtWidgets import QMessageBox


def display_message(message, office=None, month=None, path=None, emails_sent=0):
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
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Oops! Something went wrong!")
        msg.setDetailedText(message)
        msg.exec_()