'''
Lab. 1 - Resilienza di una rete di comunicazione

Membri del gruppo: Alberto Bezzon, Tommaso Carraro and Alberto Gallinaro
'''

import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import copy


sys.setrecursionlimit(100000)


def average_degree(G):
    '''
    Calcola il grado medio dei vertici del grafo orientato
    '''
    sum_degree = 0
    for node in G:
        sum_degree += len(G[node][0])
    return round(sum_degree/len(G))
        

def create_from_file():
    '''
    Genera un grafo a partire dal dataset fornito. 
    Viene utilizzata la rappresentazione del grafo con la lista delle adiacenze
    dato che il grafo è sparso
    '''
    input_file = open('as20000102.txt', 'r')        # apertura file di testo
    numLines = 0                                    # numero linee per iniziare a leggere dalla quarta linea
    graph = {}                                      # il grafo è rappresentato da un dizionario
    for i in input_file:
        numLines += 1
        if numLines > 4:
            line = i.split()
            node = line[0]
            to_node = line[1]
            if node not in graph:
                graph[node] = [[], 0]
            if to_node != node:                     # evita di inserire 'cappi'
                graph[node][0].append(to_node)
    input_file.close()
    return graph


def er(n, p):
    '''
    Implementa l'algoritmo ER (versione con grafo non orientato)

    n: numero di nodi
    p: probabilita' di inserire un arco nel grafo
    '''
    graph = {}
    arc = 0
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                a = random.random()     # estrae un numero reale casuale in [0,1)
                if i not in graph:
                    graph[i] = [[], 0]
                if j not in graph:
                    graph[j] = [[], 0]
                if a < p:
                    if j not in graph[i][0]:
                        graph[i][0].append(j)
                    if i not in graph[j][0]:
                        graph[j][0].append(i)
                    arc += 1
    print("Numero di archi con algoritmo ER: {}".format(arc))
    return graph


def upa_trial(m, num_nodes, node_numbers):
    '''
    Funzione upa trial che inizializza le variabili num_nodes e node_numbers

    m: numero di nodi del sottoinsieme a cui collegare i nuovi nodi
    num_nodes: numero di nodi del grafo
    node_numbers: lista di numeri di nodo da cui estrarre
    '''
    num_nodes = m
    node_numbers = []
    for i in range(0, m):
        for j in range(0, m):
            node_numbers.append(i)
    return num_nodes, node_numbers


def run_trial(m, num_nodes, node_numbers):
    '''
    Funzione run trial che effettua l'estrazione con reinserimento dall'urna

    m: numero di nodi del sottoinsieme a cui collegare i nuovi nodi
    num_nodes: numero di nodi del grafo
    node_numbers: lista di numeri di nodo da cui estrarre
    '''
    v1 = []
    for i in range(0, m):                   # m estrazioni dall'urna
        u = random.choice(node_numbers)     # Estrazione casuale da node_numbers
        v1.append(u)
    node_numbers.append(num_nodes)
    node_numbers.extend(v1)
    num_nodes += 1
    return v1, num_nodes, node_numbers


def upa(n, m):
    '''
    Funzione che implementa l'algoritmo UPA (versione alternativa di DPA)

    n: numero di nodi
    m: numero di nodi del sottoinsieme a cui collegare i nuovi nodi
    '''
    num_nodes = 0
    arc = 0
    node_numbers = []
    graph = {}
    for i in range(0, m):                        #  Genero un grafo di m nodi e lo rendo completo
        for j in range(0, m):
            if i not in graph:
                graph[i] = [[], 0]
            if j not in graph:
                graph[j] = [[], 0]
            if i != j:
                if j not in graph[i][0]:
                    graph[i][0].append(j)
                if i not in graph[j][0]:
                    graph[j][0].append(i)
                arc += 1
    num_nodes, node_numbers = upa_trial(m, num_nodes, node_numbers)
    for u in range(m, n):
        v1, num_nodes, node_numbers = run_trial(m, num_nodes, node_numbers)
        if u not in graph:
            graph[u] = [[], 0]
        for i in v1:
            if i not in graph[u][0]:
                graph[u][0].append(i)
            if u not in graph[i][0]:
                graph[i][0].append(u)
            arc+= 1
    print("Numero di archi con algoritmo UPA: {}".format(arc))
    return graph


def dfs_visited(graph, v, visited):
    '''
    Funzione che implementa lo pseudocodice della funzione DFS_Visited dell'Algoritmo 3.3
    '''
    graph[v][1] = 1                                     
    visited.append(v)                                   # Appendo il nodo alla componente connessa
    for v1 in graph[v][0]:                              # Scorro la lista delle adiacenze
        if graph[v1][1] == 0:                           # Se nella lista delle adiacenze trovo nodi bianchi allora ricorro su quelli
            visited = dfs_visited(graph, v1, visited)
    graph[v][1] = 2                                     # Al ritorno della ricorsione setto il colore a nero
    return visited


def connected_components(graph):
    '''
    Funzione che implementa lo pseudocodice della funzione ConnectedComponents dell'Algoritmo 3.3
    Di seguito 0 indica bianco, 1 grigio e 2 nero.
    '''
    CC = []                                     # Insieme delle componenti connesse
    for v in graph:                             # Setto il colore di tutti i nodi del grafo a bianco
        graph[v][1] = 0
    for v in graph:
        if graph[v][1] == 0:                    # Se il nodo è di colore bianco allora scorro la sua lista delle adiacenze
            comp = dfs_visited(graph, v, [])    # comp restituisce la componente connessa che contiene il nodo v passato alla funzione
            CC.append(comp)                     # Inserisco la componente connessa in CC
    return CC


def remove_node(graph, extract):
    '''
    Rimuove il nodo extract dal grafo passato come parametro
    '''
    graph.pop(extract)
    for i in graph:
        if extract in graph[i][0]:
            graph[i][0].remove(extract)


def max_connected_component_dim(cc):
    '''
    Restituisce la componente connessa maggiore
    '''
    max = 0
    for i in range(0,len(cc)):
        if max < len(cc[i]):
            max = len(cc[i])
    return max


def calculate_percentage(percentage, nodes_tot):
    '''
    Calcola la dimensione della componente connessa necessaria
    per poter definire una rete resiliente
    '''
    return round(nodes_tot*percentage/100)


def random_attack(graph):
    '''
    Simula un attacco di tipo casuale alla rete, come richiesto nella domanda 1. 
    Restituisce gli assi per la visualizzazione del grafico richiesto
    NB: la funzione risponde anche alla domanda 2
    '''
    i = 0
    resiliente = False
    x = []
    y = []
    while len(graph.keys()) != 0:                       # Continuo fino a quando non ho rimosso tutti i nodi
        max_component_size = max_connected_component_dim(connected_components(graph))
        y.append(max_component_size)
        x.append(i)
        twenty_perc = calculate_percentage(20, len(graph))
        if i == twenty_perc:                               # 20% di nodi tolti
            if max_component_size >= calculate_percentage(75, len(graph)-twenty_perc):  # 75% dei nodi ancora attivi dopo averne spenti il 20%
                resiliente = True
        i += 1
        extract = random.choice(list(graph.keys()))     # Estrazione casuale di un nodo dalla lista dei nodi
        remove_node(graph, extract)                      # Rimozione del nodo estratto dalla lista dei nodi
    y.append(max_connected_component_dim(connected_components(graph)))
    x.append(i)
    return x, y, resiliente

def take_first(elem):
    '''
    Ritorna il primo elemento della lista
    '''
    return elem[0]


def order_by_degree(graph):
    '''
    Restituisce una lista dei nodi ordinati per grado in ordine decrescente
    '''
    new_list = []
    for i in graph:
        new_list.append([len(graph[i][0]), i])
    return sorted(new_list, reverse=True, key=take_first)


def max_degree_attack(graph):
    '''
    Simula l'attacco che rimuove i nodi a partire da quello con il grado più alto
    '''
    i = 0
    resiliente = False
    x = []
    y = []
    list_ordered_by_degree = order_by_degree(graph)
    while len(graph.keys()) != 0:                   # Continuo fino a quando non ho rimosso tutti i nodi
        max_component_size = max_connected_component_dim(connected_components(graph))
        y.append(max_component_size)
        x.append(i)
        twenty_perc = calculate_percentage(20, len(graph))
        if i == twenty_perc:                               # 20% di nodi tolti
            if max_component_size >= calculate_percentage(75, len(graph)- twenty_perc):  # 75% dei nodi ancora attivi dopo averne spenti il 20%
                resiliente = True
        extract = list_ordered_by_degree[i][1]      # Seleziono di volta in volta il nodo con il grado più alto
        i += 1
        remove_node(graph, extract)                  # Rimozione del nodo estratto dalla lista dei nodi
    y.append(max_connected_component_dim(connected_components(graph)))
    x.append(i)
    return x, y, resiliente

# create_network()
graph = create_from_file()
probability = 0.0003
m = int(average_degree(graph)/2)
graph2 = er(6474, probability)
graph3 = upa(6474, m)
graph4 = copy.deepcopy(graph)
graph5 = copy.deepcopy(graph2)
graph6 = copy.deepcopy(graph3)

x, y, res = random_attack(graph)
x1, y1, res1 = random_attack(graph2)
x2, y2, res2 = random_attack(graph3)

print("\n Attacco casuale:")
print("Resilienza rete file ", res)
print("Resilienza rete ER ", res1)
print("Resilienza rete UPA", res2)

# Stampa primo grafico
plt.subplot(121)
plt.title('Attacco casuale')
plt.xlabel('Numero di nodi disattivati', fontsize=12)
plt.ylabel('Massima componente connessa', fontsize=12)
plt.plot(x, y, label='rete file')
plt.plot(x1, y1, label='ER')
plt.plot(x2, y2, label='UPA')
plt.plot([], [], ' ', label="p = " + str(probability))     # Inserisce nella legenda le etichette per m e p che non hanno associata una linea
plt.plot([], [], ' ', label="m = " + str(m))
plt.legend()

x3, y3, res3 = max_degree_attack(graph4)
x4, y4, res4 = max_degree_attack(graph5)
x5, y5, res5 = max_degree_attack(graph6)

print("\n Attacco strategico:")
print("Resilienza rete file ", res3)
print("Resilienza rete ER ", res4)
print("Resilienza rete UPA", res5)

# Stampa secondo grafico
plt.subplot(122)
plt.title('Attacco strategico')
plt.xlabel('Numero di nodi disattivati', fontsize=12)
plt.ylabel('Massima componente connessa', fontsize=12)
plt.plot(x3, y3, label='rete file')
plt.plot(x4, y4, label='ER')
plt.plot(x5, y5, label='UPA')
plt.plot([], [], ' ', label="p = " + str(probability))
plt.plot([], [], ' ', label="m = " + str(m))
plt.legend()

plt.show()