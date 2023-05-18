def breadth_first_search(graph, start, goals):
    queue = []
    visited = set()
    queue.append((start, [start]))  # Store the node and its path
    visited.add(start)

    traversal_path = []  # Store the complete traversal path

    while queue:
        node, path = queue.pop(0)
        traversal_path.append(node)  # Store the visited node in the traversal path

        if node in goals:
            return traversal_path  # Return the complete traversal path

        neighbors = graph.neighbors(node)  # Get the neighbors of the current node from the graph

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Update the path
                visited.add(neighbor)

    # If goal node is not found, return None or a custom value
    return None
