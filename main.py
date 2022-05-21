import sys
# import shutil
# import make_dir
# import split_pdf
# import send_email
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from load_gui import MainWindow, EmployeeDialog# ChooseMonthDialog

# ====================================LOAD APPLICATION=======================================#
app = QApplication(sys.argv)
app.setApplicationName("Payslips Distributor v1.0")
app.setStyle('Fusion')
home = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(590)
widget.setFixedWidth(930)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
# ====================================MAKE DIRECTORY=======================================#
# make_dir.create_dir()
# try:
#     # move payslips.pdf file to the new folder
#     shutil.move(make_dir.parent_dir + "\\payslips.pdf", make_dir.path)
#     print(f"payslips.pdf moved to the folder: {make_dir.directory}")
# except Exception as e:
#     print(e)
# ==================================SPLIT AND EXTRACT PDF==================================#
# split_pdf.extract_payslips()
# ======================================SEND EMAIL=========================================#
# send_email.email_payslip()
# ======================================EXIT APP===========================================#
# print("")
# input("Press Enter to close the program!")
# quit()
