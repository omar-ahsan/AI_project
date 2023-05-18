from collections import deque

def breadth_first_search(graph, start, goals):
    if start not in graph or not all(goal in graph for goal in goals):
        return []

    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node in goals:
            return path

        neighbors = graph[node]

        for neighbor in neighbors:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    return []
