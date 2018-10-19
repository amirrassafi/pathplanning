import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.pp_ui import Ui_MainWindow

app = QApplication(sys.argv)
mw = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mw)
mw.show()
sys.exit(app.exec_())
