import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
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

#Function to update visibility of some elements
def update_options_visibility():

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
        
# For handling the check state in reference to another for the search type
def handle_uninformed_check():
    ui.uninformed_check.setChecked(True)
    ui.informed_check.setChecked(False)

def handle_informed_check():
    ui.uninformed_check.setChecked(False)
    ui.informed_check.setChecked(True)


ui.uninformed_check.clicked.connect(handle_uninformed_check)
ui.informed_check.clicked.connect(handle_informed_check)
ui.uninformed_check.stateChanged.connect(update_options_visibility)
ui.informed_check.stateChanged.connect(update_options_visibility)

#Function for Inputs
def add_node():
    node1 = ui.node_1_input.text()
    node2 = ui.node_2_input.text()
    weight = ui.weight_input.text()

    if not node1.isalpha() or len(node1) != 1:
        show_error_message("Invalid Input for Node 1")
        return
    if not node2.isalpha() or len(node2) != 1:
        show_error_message("Invalid Input for Node 2")
        return
    if not weight.isdigit():
        show_error_message("Invalid Input for Weight")
        return
    
    
    weight = int(weight)

    ui.node_1_input.clear()
    ui.node_2_input.clear()
    ui.weight_input.clear()

    print(node1)
    print(node2)
    print(weight)

#list for goal states
goal_states = []

def submit_states():
    goal = []
    start_state = ui.start_node_input.text()
    goal = ui.goal_node_input.text()

    if not start_state.isalpha() or len(start_state) != 1:
        show_error_message("Invalid Input for Start State")
        return
    goal = goal.replace(" ", "")
    if not goal.isalpha() or len(goal) == 0:
        show_error_message("Invalid Input for Goal State")
        return
    
    goal_states.extend(list(goal))

    print(start_state)
    print(goal_states)

    ui.start_node_input.clear()
    ui.goal_node_input.clear()



def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec()

ui.add_node_button.clicked.connect(add_node)
ui.submit_button.clicked.connect(submit_states)

main_window.show()

sys.exit(app.exec())