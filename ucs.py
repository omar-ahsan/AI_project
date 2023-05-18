import networkx as nx
import heapq
from collections import defaultdict

def uniform_cost_search(graph, start, goals):
    visited = set()
    priority_queue = [(0, start, [])]  # (total_cost, current_node, path)

    traversal_path = []  # Store the complete traversal path
    path_graph = nx.Graph()  # Create an empty graph to store the path
    path_graph.add_node(start)  # Add the start node to the traversal graph

    while priority_queue:
        cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path.append(current_node)
        traversal_path.append(current_node)
        path_graph.add_node(current_node)  # Add the current node to the traversal graph

        if current_node in goals:
            for i in range(len(path) - 1):
                source = path[i]
                target = path[i + 1]
                weight = graph.get_edge_data(source, target)['weight']
                path_graph.add_edge(source, target, weight=weight)
            return path, path_graph.subgraph(path)  # Return the path and the subgraph

        if current_node in graph:
            neighbors = graph.neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    weight = graph.get_edge_data(current_node, neighbor)['weight']
                    heapq.heappush(priority_queue, (cost + weight, neighbor, path[:]))
                    path_graph.add_edge(current_node, neighbor, weight=weight)  # Add the edge to the traversal graph

    return None, None  # No path found, return an empty path and empty graph
