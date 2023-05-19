import networkx as nx
import heapq

def a_star_search(graph, start_state, goal_states, heuristic):
    visited = set()
    queue = [(0, start_state, [])]  # (total_cost, current_node, path)
    is_directed = graph.is_directed()
    traversal_path = []  # Store the complete traversal path
    path_graph = nx.DiGraph() if is_directed else nx.Graph()  # Create an empty directed/undirected graph
    path_graph.add_node(start_state)  # Add the start node to the traversal graph

    while queue:
        total_cost, current_state, path = heapq.heappop(queue)
        

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
                if not graph.is_directed():
                    path_graph.add_edge(target, source, weight=weight)  # Add the reverse edge for undirected graphs
            return path, path_graph.subgraph(path)  # Return the traversal path and the subgraph

        if current_state in graph:
            neighbors = graph[current_state]
            for neighbor_state, edge_data in neighbors.items():
                if neighbor_state not in visited:
                    neighbor_cost = total_cost + edge_data['weight']
                    priority = neighbor_cost + heuristic(neighbor_state)
                    heapq.heappush(queue, (priority, neighbor_state, path[:]))
                    path_graph.add_edge(current_state, neighbor_state, weight=edge_data['weight'])  # Add the edge to the traversal graph
                    if not graph.is_directed():
                        path_graph.add_edge(neighbor_state, current_state, weight=edge_data['weight'])  # Add the reverse edge for undirected graphs

    return None, None  # No path found, return an empty path and empty graph
