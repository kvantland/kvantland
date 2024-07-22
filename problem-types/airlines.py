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
	try:
		graph = build_graph(answer)
		
		for node in graph:
			if len(node) > 4:
				return False
			distances = bfs_shortest_path(graph, node)
			print(distances)
			for other_node in graph:
				if distances[other_node] > data['transfers'] + 1:
					return False
		if (len(answer) > len(graph) - 1): #Check if graph is tree
			return False
		return True
	except:
		return False
