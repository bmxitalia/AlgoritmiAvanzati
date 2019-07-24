'''
Lab. 1 - Resilienza di una rete di comunicazione
Members of group: Alberto Bezzon and Tommaso Carraro
'''

# La rete e' composta da 6474 nodi e 13233 archi non orientati, pertanto il 
# grafo e' sparso e la rappresentazione migliore e' tramite la lista delle adiacenze.

import matplotlib.pyplot as plt
import random
'''
def DFS_visited(G, u, visited):
    G.get(u)[1][0] = 1
    visited.append(u)
    for node in G.get(u)[0]:
        if G.get(node)[1][0] == 0:
            visited = DFS_visited(G, node, visited)
    G.get(u)[1][0] = 2
    return visited

# 0: bianco, 1: grigio, 2: nero
def connected_components(G):
    for node in G:
        G.get(node)[1][0] = 0
    CC = list()
    for node in G:
        if G.get(node)[1][0] == 0:
            comp = DFS_visited(G, node, [])
            CC.append(comp)
    return CC


def shutdown_node(G, node):
    if node in G:
        del G[node]
        for u in G:
            if node in G.get(u)[0]:
                G.get(u)[0].remove(node)
        

def attack(G):
    while len(G) != 0:
        number = random.choice(list(G.keys()))
        shutdown_node(G, number)


with open('as20000102.txt', 'r') as input_file:
    # Scarto le prime 4 righe del dataset
    for i in range(0,5):
        line = input_file.readline()
    graph = dict()
    while line:
        arc = line.split()
        if arc[0] != arc[1]:
            if arc[0] in graph:
                graph.get(arc[0])[0].append(arc[1])
            else:
                graph.update({arc[0]:[[arc[1]],[0]]})
        line = input_file.readline()
    #print(connected_components(graph))
    attack(graph)
    #connected_components(graph)
    #print(graph.get('1'))
'''

# UPA

num_nodes = 0
node_numbers = []

def dpa_trial(m):
    global num_nodes
    global node_numbers
    num_nodes = m
    node_numbers = []
    for i in range (0, m):
        for j in range(0, m):
            node_numbers.append(i)


def run_trial(m):
    global num_nodes
    V = []
    for i in range(1, m):
        u = random.choice(node_numbers) # Seleziono casualmente un elemento dalla lista
        node_numbers.remove(u) # Estraggo l'elemento da node_numbers
        V.append(u)
    node_numbers.append(num_nodes)
    node_numbers.extend(V)
    num_nodes += 1
    return V


def dpa(n, m):
    '''
    n: # nodi
    m: valore intero tale che 1<=m<=n
    '''
    G = dict()
    # Grafo con m nodi
    for i in range(0, m):
        G.update({i:[[], 0]})
    # Rendo il grafo completo
    for u in G:
        for v in G:
            if u != v:
                G.get(u)[0].append(v)
    dpa_trial(m)
    for u in range(m, n):
        V = run_trial(m)
        G.update({u:[[v for v in V], 0]})
    return G


graph = dpa(20, 10) 
print(graph)