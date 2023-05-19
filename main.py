import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene
import gui
import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


#Importing algorithms
import bfs
import dfs
import dls
import ucs
import bds
import ids
import astar
import bestfs


app = QApplication(sys.argv)
main_window = QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(main_window)

#--------------------------------------------Direction function---------------------------------------#
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
        # Clear graph view
        clear_graph_view()
        # Clear the graph
        graph = None

    direction_selected = new_direction

#--------------------------------------------Visibility of elements---------------------------------------#
# Hidden elements before check
# Uninformed Search
ui.uninformed_search_label.setVisible(False)
ui.uninformed_combo.setVisible(False)
ui.uninformed_depth_label.setVisible(False)
ui.uninformed_depth_input.setVisible(False)

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
    uninformed_option = ui.uninformed_combo.currentText()

    # For Uninformed
    if ui.uninformed_check.isChecked():
        ui.uninformed_search_label.setVisible(True)
        ui.uninformed_combo.setVisible(True)

        if uninformed_option == "Depth Limited" or uninformed_option == "Iterative Deepening":
            ui.uninformed_depth_label.setVisible(True)
            ui.uninformed_depth_input.setVisible(True)
        else:
            ui.uninformed_depth_label.setVisible(False)
            ui.uninformed_depth_input.setVisible(False)
        

    elif ui.uninformed_check.isCheckable(): 
        ui.uninformed_search_label.setVisible(False)
        ui.uninformed_combo.setVisible(False)
        ui.uninformed_depth_label.setVisible(False)
        ui.uninformed_depth_input.setVisible(False)
        

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
    update_options_visibility()

def handle_informed_check():
    ui.uninformed_check.setChecked(False)
    ui.informed_check.setChecked(True)


ui.uninformed_check.clicked.connect(handle_uninformed_check)
ui.informed_check.clicked.connect(handle_informed_check)
ui.uninformed_check.stateChanged.connect(update_options_visibility)
ui.informed_check.stateChanged.connect(update_options_visibility)
ui.uninformed_combo.currentIndexChanged.connect(update_options_visibility)

#--------------------------------------------Input Boxes---------------------------------------#
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

goal_states = []

# Function for start and goal state
def submit_states():
    global start_state, goal_states
    goal = []
    goal_states = []
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


heuristics_dict = {}

#Function to add heuristics if informed is checked
def add_heuristic():
    global heuristic_value, heuristic_node, heuristics_dict
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
    

    heuristics_dict[heuristic_node] = int(heuristic_value)
    print(heuristics_dict)

    ui.informed_node_input.clear()
    ui.informed_heuristic_input.clear()


#--------------------------------------------Graph---------------------------------------#
# Display graph function
def initiate_graph():
    if graph is not None:
        clear_graph_view()
        connect_graph(draw_graph)
    else:
        show_error_message("Graph is empty. Add nodes first")

# Draw graph function
def draw_graph(fig):
    pos = graphviz_layout(graph, prog='dot')

    node_size = 200
    node_color = "red"
    node_font_color = "white"
    edge_color = "black"

    ax = fig.add_subplot(111)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=node_size, node_color=node_color, edgecolors="black")
    nx.draw_networkx_labels(graph, pos, ax=ax, font_color=node_font_color)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_color)

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    ax.axis("off")
    plt.tight_layout()

#--------------------------------------------Path---------------------------------------#
# Function to check the selection of Informed or Uninformed search type and generate path according to it.
def generate_path():
    global heuristics_dict
    search_type = ""

    if ui.uninformed_check.isChecked():
        search_type = "Uninformed"
        uninformed_option = ui.uninformed_combo.currentText()
        print("Uninformed Search Type:", uninformed_option)

    elif ui.informed_check.isChecked():
        search_type = "Informed"
        informed_option = ui.informed_combo.currentText()
        print("Informed Search Type:", informed_option)
    
    if search_type == "":
        show_error_message("Please select a search type")
        return

    if graph is None or len(graph.nodes) == 0:
        show_error_message("Graph is empty. Add nodes first")
        return

    # Generate path based on search type and options
    if search_type == "Uninformed":

        if uninformed_option == "Breadth First Search":
            path, path_graph = bfs.breadth_first_search(graph, start_state, goal_states)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        if uninformed_option == "Depth First Search":
            path, path_graph = dfs.depth_first_search(graph, start_state, goal_states)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        if uninformed_option == "Depth Limited":
            depth = ui.uninformed_depth_input.text()
            if not depth.isdigit():
                show_error_message("Invalid Input for Depth")
                return

            depth = int(depth)
            print(depth)
            path, path_graph = dls.depth_limited_search(graph, start_state, goal_states, depth)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        if uninformed_option == "Uniform Cost Search":
            path, path_graph = ucs.uniform_cost_search(graph, start_state, goal_states)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        if uninformed_option == "Iterative Deepening":
            depth = ui.uninformed_depth_input.text()
            if not depth.isdigit():
                show_error_message("Invalid Input for Depth")
                return

            depth = int(depth)
            print(depth)
            path, path_graph = ids.iterative_deepening_search(graph, start_state, goal_states, depth)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found") 

        if uninformed_option == "Bidirectional Search":
            path, path_graph = bds.bidirectional_search(graph, start_state, goal_states)
            if path and path_graph:
                print("Path: ", path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        pass
    elif search_type == "Informed":

        if informed_option == "A*":
            heuristic = lambda state: heuristics_dict.get(state, float('inf'))
            print(heuristic)
            path, path_graph = astar.a_star_search(graph, start_state, goal_states, heuristic)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")

        if informed_option == "Best First":
            heuristic = lambda state: heuristics_dict.get(state, float('inf'))
            print(heuristic)
            path, path_graph = bestfs.best_first_search(graph, start_state, goal_states, heuristic)
            if path and path_graph:
                print("Path: " , path)
                write_path(path)
                initiate_path(path_graph)
            else:
                show_error_message("No path found")
        pass

def initiate_path(path_graph):
    if path_graph is not None:
        connect_graph(lambda fig: draw_path(fig, path_graph))
    else:
        show_error_message("No path found")

def draw_path(fig, path_graph):
    pos = graphviz_layout(path_graph, prog='dot')
    edge_labels = nx.get_edge_attributes(path_graph, 'weight')

    ax = fig.add_subplot(111)
    nx.draw(path_graph, pos, with_labels=True, ax=ax)
    nx.draw_networkx_edge_labels(path_graph, pos, edge_labels=edge_labels, ax=ax)

    plt.tight_layout()

def write_path(path):
    path_str = ' -> '.join(path)  # Convert the list of nodes to a string
    print(path_str)
    ui.path_line_box.setText(path_str)  # Set the text of the path_box to the generated path


#--------------------------------------------Graph View---------------------------------------#

def connect_graph(draw_func):
    fig = plt.figure()
    # send an empty fig to draw_func
    draw_func(fig)
    # receive the fig and place it into canvas
    canvas = FigureCanvas(fig)
    # initiate a new scene
    scene = QGraphicsScene()
    # add the canvas into the scene
    scene.addWidget(canvas)
    # connect the graph_view object to scene
    ui.graph_view.setScene(scene)

#--------------------------------------------Clearing---------------------------------------#
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
    ui.path_line_box.setText("")
    print("Variables cleared")

# Clear graph view with reference to restrictions
def clear_graph_view():
    scene = ui.graph_view.scene()
    if scene is not None:
        items = scene.items()
        for item in items:
            scene.removeItem(item)


#--------------------------------------------Error/Warning Box---------------------------------------#
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


#--------------------------------------------Connects---------------------------------------#
ui.informed_heuristic_button.clicked.connect(add_heuristic)
ui.add_node_button.clicked.connect(add_node)
ui.submit_button.clicked.connect(submit_states)
ui.direction_combo.currentIndexChanged.connect(select_direction)
ui.graph_button.clicked.connect(initiate_graph)
ui.path_button.clicked.connect(generate_path)

main_window.show()

sys.exit(app.exec())