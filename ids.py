import networkx as nx

def iterative_deepening_search(graph, start, goals, depth_limit):
    path_graph = nx.Graph()  # Create an empty graph to store the path
    traversal_path = []  # Store the complete traversal path

    for limit in range(depth_limit+1):
        visited = set()
        stack = [(start, [start], 0)]  # Store the node, its path, and the current depth

        while stack:
            node, path, depth = stack.pop()
            visited.add(node)

            if depth <= limit:
                traversal_path.append(node)  # Store the visited node in the traversal path
                path_graph.add_node(node)  # Add the visited node to the path graph

                if node in goals:
                    for i in range(len(path) - 1):
                        source = path[i]
                        target = path[i + 1]
                        weight = graph[source][target]['weight']  # Get the weight of the edge
                        path_graph.add_edge(source, target, weight=weight)
                    return traversal_path, path_graph.subgraph(traversal_path)  # Return the complete traversal path and the subgraph

                neighbors = graph.neighbors(node)  # Get the neighbors of the current node from the graph
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], depth + 1))  # Update the path and depth
                        visited.add(neighbor)
                        weight = graph[node][neighbor]['weight']  # Get the weight of the edge
                        path_graph.add_edge(node, neighbor, weight=weight)  # Add the edge with its weight to the path graph

    # If goal node is not found, return None or a custom value
    return None, None
