import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from load_gui import MainWindow

# ====================================LOAD APPLICATION=======================================#
app = QApplication(sys.argv)
app.setApplicationName("Payslips Distributor v1.2")
app.setStyle("Fusion")
home = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(650)
widget.setFixedWidth(1050)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
