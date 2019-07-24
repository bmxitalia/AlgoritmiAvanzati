import random
from collectios import Counters

graph = {
    0: [1, 2, 3],
    1: [],
    2: [1, 11],
    3: [4, 5],
    4: [3, 5],
    5: [3, 4, 7],
    6: [8],
    7: [],
    8: [9],
    9: [],
    11: []
}

# Disable random node in the graph
def disableRandomNode(graph):
    min = 0
    max = len(graph.keys())

    n = random.randint(min, max)
    while graph[n] == []:
        n = random.randint(min, max)

    graph[n] = []

    return graph


print(disableRandomNode(graph))


# Disable the node with the maximum degree, assume that there are no hooks, otherwise just "-1" the max degree computed
def disableMaxDegreeNode(graph):
    flat = []
    maxDegree = [0,0] #degree, nodeNumber
    
    # flat out the dictionary
    for node in graph:
        flat.extend(graph[node])
    
    print(flat)
    degrees = Counter(flat)

    for node in graph:
        deg = degrees[node]
        if deg > maxDegree[0]:
            maxDegree = [deg, node]


    return maxDegree

