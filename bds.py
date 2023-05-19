import networkx as nx

def bidirectional_search(graph, start, goals):
    queue_forward = []
    queue_backward = []
    visited_forward = set()
    visited_backward = set()

    queue_forward.append((start, [start]))  # Store the node and its path
    queue_backward.append((goals[0], [goals[0]]))  # Store the node and its path

    visited_forward.add(start)
    visited_backward.add(goals[0])

    traversal_path = []  # Store the complete traversal path
    path_graph = nx.Graph()  # Create an empty graph to store the path

    meeting_node = None  # Initialize meeting_node to None

    while queue_forward and queue_backward:
        # Forward BFS
        node_forward, path_forward = queue_forward.pop(0)
        traversal_path.append(node_forward)  # Store the visited node in the traversal path
        path_graph.add_node(node_forward)  # Add the visited node to the path graph

        if node_forward in visited_backward:
            meeting_node = node_forward
            break

        neighbors_forward = graph.neighbors(node_forward)  # Get the neighbors of the current node from the graph

        for neighbor_forward in neighbors_forward:
            if neighbor_forward not in visited_forward:
                queue_forward.append((neighbor_forward, path_forward + [neighbor_forward]))  # Update the path
                visited_forward.add(neighbor_forward)
                weight = graph.get_edge_data(node_forward, neighbor_forward)['weight']  # Get the weight of the edge
                path_graph.add_edge(node_forward, neighbor_forward, weight=weight)  # Add the edge with its weight to the path graph

        # Backward BFS
        node_backward, path_backward = queue_backward.pop(0)
        traversal_path.append(node_backward)  # Store the visited node in the traversal path
        path_graph.add_node(node_backward)  # Add the visited node to the path graph

        if node_backward in visited_forward:
            meeting_node = node_backward
            break

        neighbors_backward = graph.neighbors(node_backward)  # Get the neighbors of the current node from the graph

        for neighbor_backward in neighbors_backward:
            if neighbor_backward not in visited_backward:
                queue_backward.append((neighbor_backward, path_backward + [neighbor_backward]))  # Update the path
                visited_backward.add(neighbor_backward)
                weight = graph.get_edge_data(node_backward, neighbor_backward)['weight']  # Get the weight of the edge
                path_graph.add_edge(node_backward, neighbor_backward, weight=weight)  # Add the edge with its weight to the path graph

    if meeting_node is not None:
        # Combine the forward and backward paths
        if meeting_node in path_forward:
            forward_path = path_forward[:path_forward.index(meeting_node) + 1]
        else:
            forward_path = []
        if meeting_node in path_backward:
            backward_path = path_backward[:path_backward.index(meeting_node)][::-1]
        else:
            backward_path = []
        combined_path = forward_path + backward_path[1:]  # Exclude the meeting node from the backward path
        for i in range(len(combined_path) - 1):
            source = combined_path[i]
            target = combined_path[i + 1]
            weight = graph.get_edge_data(source, target)['weight']
            path_graph.add_edge(source, target, weight=weight)
        return traversal_path, path_graph.subgraph(traversal_path)  # Return the complete traversal path and the subgraph

    # If goal node is not found, return None or a custom value
    return None, None
