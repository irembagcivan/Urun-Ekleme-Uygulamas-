import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from arayuz import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

sys.exit(uygulama.exec_())
