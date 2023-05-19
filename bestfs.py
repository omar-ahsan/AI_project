import networkx as nx
import heapq

def best_first_search(graph, start_state, goal_states, heuristic):
    visited = set()
    queue = [(heuristic(start_state), start_state, [])]  # (heuristic_value, current_node, path)

    traversal_path = []  # Store the complete traversal path
    path_graph = nx.Graph()  # Create an empty graph to store the path
    path_graph.add_node(start_state)  # Add the start node to the traversal graph

    while queue:
        _, current_state, path = heapq.heappop(queue)

        if current_state in visited:
            continue

        visited.add(current_state)
        path.append(current_state)
        traversal_path.append(current_state)
        path_graph.add_node(current_state)  # Add the current state to the traversal graph

        if current_state in goal_states:
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                weight = graph.get_edge_data(source, target)['weight']
                path_graph.add_edge(source, target, weight=weight)
            return traversal_path, path_graph.subgraph(traversal_path)  # Return the traversal path and the subgraph

        if current_state in graph:
            neighbors = graph[current_state]
            for neighbor_state, edge_data in neighbors.items():
                if neighbor_state not in visited:
                    priority = heuristic(neighbor_state)
                    heapq.heappush(queue, (priority, neighbor_state, path[:]))
                    path_graph.add_edge(current_state, neighbor_state, weight=edge_data['weight'])  # Add the edge to the traversal graph

    return None, None  # No path found, return an empty path and empty graph


