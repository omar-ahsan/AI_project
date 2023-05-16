import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import gui

app = QApplication(sys.argv)
main_window = QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(main_window)

# Hidden elements before check
# Uninformed Search
ui.uninformed_search_label.setVisible(False)
ui.uninformed_combo.setVisible(False)

# Informed Search
ui.informed_combo.setVisible(False)
ui.informed_heuristic_button.setVisible(False)
ui.informed_heuristic_input.setVisible(False)
ui.informed_heuristic_label.setVisible(False)
ui.informed_search_label.setVisible(False)
ui.informed_node_input.setVisible(False)
ui.informed_node_label.setVisible(False)


def update_options_visibility(state):

    # For Uninformed
    if ui.uninformed_check.isChecked():
        ui.uninformed_search_label.setVisible(True)
        ui.uninformed_combo.setVisible(True)

    elif ui.uninformed_check.isCheckable(): 
        ui.uninformed_search_label.setVisible(False)
        ui.uninformed_combo.setVisible(False)

    # For Informed
    if ui.informed_check.isChecked():
        ui.informed_combo.setVisible(True)
        ui.informed_heuristic_button.setVisible(True)
        ui.informed_heuristic_input.setVisible(True)
        ui.informed_heuristic_label.setVisible(True)
        ui.informed_search_label.setVisible(True)
        ui.informed_node_input.setVisible(True)
        ui.informed_node_label.setVisible(True)

    elif ui.informed_check.isCheckable():
        ui.informed_combo.setVisible(False)
        ui.informed_heuristic_button.setVisible(False)
        ui.informed_heuristic_input.setVisible(False)
        ui.informed_heuristic_label.setVisible(False)
        ui.informed_search_label.setVisible(False)
        ui.informed_node_input.setVisible(False)
        ui.informed_node_label.setVisible(False)

ui.uninformed_check.stateChanged.connect(update_options_visibility)
ui.informed_check.stateChanged.connect(update_options_visibility)


main_window.show()

sys.exit(app.exec())