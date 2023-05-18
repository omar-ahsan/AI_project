import networkx as nx

def depth_limited_search(graph, start, goals, depth_limit):
    visited = set()
    stack = [(start, [start], 0)]  # Store the node, its path, and depth
    visited.add(start)

    traversal_path = []  # Store the complete traversal path

    path_graph = nx.Graph()  # Create an empty graph to store the path

    while stack:
        node, path, depth = stack.pop()
        traversal_path.append(node)  # Store the visited node in the traversal path
        path_graph.add_node(node)  # Add the visited node to the path graph

        if node in goals:
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                weight = graph.get_edge_data(source, target)['weight']
                path_graph.add_edge(source, target, weight=weight)
            return traversal_path, path_graph.subgraph(traversal_path)  # Return the complete traversal path and the subgraph

        if depth < depth_limit:
            neighbors = graph.neighbors(node)  # Get the neighbors of the current node from the graph

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], depth + 1))  # Update the path and depth
                    visited.add(neighbor)
                    weight = graph.get_edge_data(node, neighbor)['weight']  # Get the weight of the edge
                    path_graph.add_edge(node, neighbor, weight=weight)  # Add the edge with its weight to the path graph

    # If goal node is not found within the depth limit, return None or a custom value
    return None, None
