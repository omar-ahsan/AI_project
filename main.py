import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import gui
import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt


app = QApplication(sys.argv)
main_window = QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(main_window)

#Graph Variable
graph = None

#Direction variable and function
direction_selected = "Undirected Graph"

def select_direction(index):
    global direction_selected, graph

    new_direction = ui.direction_combo.itemText(index)

    if direction_selected != "" and direction_selected != new_direction:
        if not show_warning_message("Changing the direction will clear all nodes. Are you sure?"):
            # User canceled, revert to previous direction
            ui.direction_combo.setCurrentText(direction_selected)
            return

        # Clear all inputs and stored values
        ui.node_1_input.clear()
        ui.node_2_input.clear()
        ui.weight_input.clear()
        ui.start_node_input.clear()
        ui.goal_node_input.clear()

        # Clear the stored goal states
        clear_variables()
        # Clear the graph
        graph = None

    direction_selected = new_direction

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
    global node1, node2, weight, graph

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

    print(node1)
    print(node2)
    print(weight)

    if graph is None:
        if direction_selected == "Undirected Graph":
            graph = nx.Graph()
        else:
            graph = nx.DiGraph()

    graph.add_edge(node1, node2, weight=weight)

    if direction_selected == "Undirected Graph":
        graph.add_edge(node2, node1, weight=weight)

    clear_graph_view()
    ui.node_1_input.clear()
    ui.node_2_input.clear()
    ui.weight_input.clear()


# Display graph function
def display_graph():
    if graph is not None:
        clear_graph_view()
        draw_graph()
    else:
        show_error_message("Graph is empty. Add nodes first")

# Draw graph function
def draw_graph():
    if graph is None:
        show_error_message("Graph is empty. Add nodes first")
        return

    pos = nx.spring_layout(graph)

    node_size = 200
    node_color = "red"
    node_font_color = "white"
    edge_color = "black"

    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=node_size, node_color=node_color, edgecolors="black")
    nx.draw_networkx_labels(graph, pos, ax=ax, font_color=node_font_color)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_color)

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    ax.axis("off")
    plt.tight_layout()
    plt.show()

goal_states = []

# Function for start and goal state
def submit_states():
    global start_state
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


#Function to add heuristics if informed is checked
def add_heuristic():
    global heuristic_value, heuristic_node
    heuristic_node = ui.informed_node_input.text()
    heuristic_value = ui.informed_heuristic_input.text()

    if not heuristic_node.isalpha() or len(heuristic_node) != 1:
        show_error_message("Invalid Input for Node 1")
        return
    if not heuristic_value.isdigit():
        show_error_message("Invalid Input for Weight")
        return
    
    heuristic_value = int(heuristic_value)

    print(heuristic_node)
    print(heuristic_value)

    ui.informed_node_input.clear()
    ui.informed_heuristic_input.clear()

# Function to clear all inputs for changing of direction
def clear_variables():
    global node1, node2, weight, start_state, goal_states, heuristic_node, heuristic_value
    node1 = ""
    node2 = ""
    weight = ""
    start_state = ""
    goal_states = []
    heuristic_node = ""
    heuristic_value = ""
    print("Variables cleared")

# Clear graph view with reference to restrictions
def clear_graph_view():
    scene = ui.graph_view.scene()
    if scene is not None:
        items = scene.items()
        for item in items:
            scene.removeItem(item)


# Error msg for invalid input
def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec()

# Warning msg for changing of direction
def show_warning_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("Warning")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
    return msg_box.exec() == QMessageBox.StandardButton.Yes

ui.informed_heuristic_button.clicked.connect(add_heuristic)
ui.add_node_button.clicked.connect(add_node)
ui.submit_button.clicked.connect(submit_states)
ui.direction_combo.currentIndexChanged.connect(select_direction)
ui.graph_button.clicked.connect(display_graph)

main_window.show()

sys.exit(app.exec())