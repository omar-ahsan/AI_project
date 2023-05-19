import networkx as nx

def breadth_first_search(graph, start, goals):
    queue = []
    visited = set()
    queue.append((start, [start]))  # Store the node and its path
    visited.add(start)

    is_directed = graph.is_directed()

    traversal_path = []  # Store the complete traversal path

    path_graph = nx.DiGraph() if is_directed else nx.Graph()  # Create an empty directed/undirected graph

    while queue:
        node, path = queue.pop(0)
        traversal_path.append(node)  # Store the visited node in the traversal path
        path_graph.add_node(node)  # Add the visited node to the path graph

        if node in goals:
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                weight = graph.get_edge_data(source, target)['weight']
                path_graph.add_edge(source, target, weight=weight)
                if not is_directed:
                    path_graph.add_edge(target, source, weight=weight)  # Add the reverse edge for undirected graphs
            return traversal_path, path_graph.subgraph(traversal_path)  # Return the complete traversal path and the subgraph

        neighbors = graph.neighbors(node)  # Get the neighbors of the current node from the graph

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Update the path
                visited.add(neighbor)
                weight = graph.get_edge_data(node, neighbor)['weight']  # Get the weight of the edge
                path_graph.add_edge(node, neighbor, weight=weight)  # Add the edge with its weight to the path graph
                if not is_directed:
                    path_graph.add_edge(neighbor, node, weight=weight)  # Add the reverse edge for undirected graphs

    # If goal node is not found, return None or a custom value
    return None, None
