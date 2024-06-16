def build_graph(data):
    graph = {}
    for node1, node2 in data:
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph

def bfs_shortest_path(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [start]
    
    while queue:
        current = queue.pop(0)
        current_distance = distances[current]
        
        for neighbor in graph[current]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = current_distance + 1
                queue.append(neighbor)
    
    return distances

def validate(data, answer):
    # Build the graph
    graph = build_graph(answer)
    
    # Check connectivity and shortest path condition
    for node in graph:
        distances = bfs_shortest_path(graph, node)
        for other_node in graph:
            if distances[other_node] >= data['correct']:
                return False
    
    return True
