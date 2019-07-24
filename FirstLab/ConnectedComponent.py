graph = {
    0: [1, 2, 3],
    1: [],
    2: [1, 2, 11],
    3: [3, 4, 5],
    4: [3, 4, 5],
    5: [3, 4, 5, 7],
    6: [6, 8],
    7: [],
    8: [8, 9],
    9: [],
    11: []
}


def getConnectedComponents(graph):
    visited = []
    result = []
    for node in graph:
        if node not in visited:
            connComponent, v = connectedComponent(node, visited, graph)
            visited.extend(v)
            result.append(connComponent)

    return result


def connectedComponent(node, visited, graph):
    queue = []
    result = []
    queue.extend(graph[node])
    visited.append(node)
    result.append(node)
    while queue:
        node = queue.pop()
        print(node)
        if node not in visited:
            queue.extend(graph[node])
            visited.append(node)
            result.append(node)

    return result, queue


print(getConnectedComponents(graph))