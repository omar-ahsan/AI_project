import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import gui

app = QApplication(sys.argv)
main_window = QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(main_window)

main_window.show()

sys.exit(app.exec())