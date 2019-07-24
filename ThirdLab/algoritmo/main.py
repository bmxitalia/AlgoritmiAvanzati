import time
import copy
import math
import sys
import csv

sys.setrecursionlimit(50000)

RRR = 6378.388
START_TIME = 0
CUTOFF = 0


def read_csv_distances():
    dist = [15, 494, 1001, 52, 230, 101, 23]
    i = 0
    distances = {}
    with open('distances.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['graph'] in distances:
                distances[row['graph']]['dist'][row['key']] = int(row['distance'])
            else:
                distances[row['graph']] = {
                    'nodes': list(range(1, dist[i])),
                    'dist': {row['key']: int(row['distance'])}
                }
                i += 1
    return distances


def take_distance(v1, v2, name):
    key = str(v1) + "|" + str(v2)
    return distances[name]['dist'][key]


# restituisce il nodo del grafo che non fa parte del circuito parziale e che minimizza la distanza da uno qualsiasi dei nodi nel circuito parziale
def take_min(list, toBeInserted, graph_name):
    min_ = sys.maxsize
    k_min = -1
    for k in toBeInserted:
        if k in k_dict:
            dist = take_distance(min_k[-1], k, graph_name)
            if dist < k_dict[k]:
                k_dict[k] = dist
        else:
            for i in list:
                dist = take_distance(k, i, graph_name)
                if dist < min_:
                    min_ = dist
                    k_min = k
            k_dict[k_min] = min_
    k_min = min(k_dict, key=k_dict.get)
    k_dict.pop(k_min)
    min_k.append(k_min)
    return k_min


def closest_insertion(G):
    # inizializzazione
    partialCircuit = [1]  # lista che contiene i nodi presenti nel circuito
    toBeInserted = list(range(2, len(distances[G]['nodes']) + 1))
    min_ = sys.maxsize
    v = -1
    # ricerca del minimo vertice
    for i in toBeInserted:
        dist = take_distance(1, i, G)
        if dist < min_:
            min_ = dist
            v = i

    partialCircuit.append(v)
    partialCircuit.append(1)  # chiusura circuito Hamiltoniano
    toBeInserted.remove(v)  # rimozione del nodo inserito dai nodi da inserire
    # inizio cicli di selezione e inserimento
    while len(toBeInserted) > 0:
        j_min = -1
        min_ = sys.maxsize
        k_min = take_min(partialCircuit, toBeInserted, G)
        for i in range(0, len(partialCircuit) - 1):
            j = i + 1
            dist = take_distance(partialCircuit[i], k_min, G) + take_distance(k_min,
                                                                    partialCircuit[j], G) - take_distance(partialCircuit[i],
                                                                                                    partialCircuit[j], G)
            if dist < min_:
                min_ = dist
                j_min = j
        partialCircuit.insert(j_min, k_min)
        toBeInserted.remove(k_min)
    solution = cost(partialCircuit, G)
    print("Closest Insertion:", solution)
    print("Error: ", ((solution - solutions[G]) / solutions[G]) * 100)


def nearest_neighbor(G):
    circ = [1]
    toBeInserted = list(range(2, len(distances[G]['nodes']) + 1))
    insert = -1
    while toBeInserted:
        min_ = sys.maxsize
        vk = circ[-1]
        for i in toBeInserted:
            dist = take_distance(vk, i, G)
            if dist < min_:
                min_ = dist
                insert = i
        circ.append(insert)
        toBeInserted.remove(insert)
    circ.append(1)
    solution = cost(circ, G)
    print("Cost: ", solution)
    print("Error: ", ((solution - solutions[G]) / solutions[G]) * 100)


def get_range(v, s):
    arr = copy.deepcopy(s)
    arr.remove(v)
    return arr


def hk_visit(v, S, d, pi, graph_name):
    # if the execution time has exeeded cutoff, stop the program
    now = time.time()
    if now - START_TIME > CUTOFF:
        return 0

    if S[0] == v and len(S) == 1:
        return take_distance(v, 1, graph_name)
    else:
        key = str(v) + "|" + str(S)
        if key in d.keys():
            return d[key]
        else:
            mindist = math.inf
            minprec = None
            list_without = get_range(v, S)
            for u in list_without:
                dist = hk_visit(u, list_without, d, pi, graph_name)
                if dist == 0:
                    break
                if (dist + take_distance(u, v, graph_name)) < mindist:
                    mindist = dist + take_distance(u, v, graph_name)
                    minprec = u
            key = str(v) + "|" + str(S)
            d[key] = mindist
            pi[key] = minprec
            return mindist


def hk_tsp(t, graph_name):
    # set start time and termination time
    global START_TIME
    global CUTOFF
    CUTOFF = t * 60
    START_TIME = time.time()

    d = {}
    pi = {}
    solution = hk_visit(1, distances[graph_name]['nodes'], d, pi, graph_name)
    print("Exact: ", solution)
    print("Error: ", ((solution - solutions[graph_name])/solutions[graph_name]) * 100)


def cost(circuit, graph_name):
    dist_sum = 0
    for i in range(0, len(circuit)-1):
        dist_sum += take_distance(circuit[i], circuit[i + 1], graph_name)
    return dist_sum


# restituisce i figli di un nodo nell'albero di copertura minimo
def findChildren(node, sol):
    list_of_sons = []
    for n in list(sol.keys()):
        if sol[n] == node:
            list_of_sons.append(n)

    return list_of_sons


def Prim(graph_name):
    queue = {}  # Dictionary that represent the queue
    nodeList = []
    key = {}
    pi = {}
    for node in distances[graph_name]['nodes']:
        if node == 1:
            nodeList.append([1, 0])
            key[1] = 0
            queue[node] = 0
        else:
            nodeList.append([node, math.inf])
            key[node] = math.inf
            queue[node] = math.inf
        pi[node] = None

    while len(queue) > 0:
        u = min(queue, key=queue.get) # extract the key with minimum value in queue
        queue.pop(u)
        # list_without = get_range(u, distances[graph_name]['nodes'])
        # questo loop è ciò che rallenta l'algoritmo
        for v in distances[graph_name]['nodes']:
            if u == v:
                continue
            uv = take_distance(u, v, graph_name)
            if v in queue and uv < key[v]:
                key[v] = uv
                pi[v] = u
                queue[v] = key[v]

    #list_without_start = get_range(1, distances[graph_name]['nodes'])
    A = {}
    for node in distances[graph_name]['nodes']:
        if node == 1:
            continue
        A[node] = pi[node]

    return A


def walkthrough(node, tree):
    if len(tree[node]) == 0:
        return "" + str(node)

    res = ""
    for adj in tree[node]:
        res += "-" + str(walkthrough(adj, tree))
    return str(node) + res


def MST_Prim(graph_name):
    sol = Prim(graph_name)
    tree = {}
    tree[1] = findChildren(1, sol) # 1 non ha nessun padre e quindi non compare nella lista delle chiavi, quindi va fatto a parte
    for node in list(sol.keys()):
        tree[node] = findChildren(node, sol)
    # After this cycle, nodes are inserted in a dictionary

    path = walkthrough(1, tree) # il path è la sequenza di come i nodi devono essere visitati per la costruzione del circuito hamiltoniano
    path += "-" + str(1) # chiusura del circuito hamiltoniano
    circuit = path.split("-") # circuito sottoforma di lista

    # Convert string to a list of int to reuse cost() function
    c = [int(x) for x in circuit]

    solution = cost(c, graph_name)
    print("2-approximate with minimum spanning tree:", solution)
    print("Error: ", ((solution - solutions[graph_name]) / solutions[graph_name]) * 100)

    return path


if __name__ == '__main__':
    distances = read_csv_distances()
    solutions = {'burma14.tsp': 3323, 'ulysses22.tsp': 7013, 'eil51.tsp': 426, 'kroD100.tsp': 21294, 'gr229.tsp': 134602, 'd493.tsp': 35002, 'dsj1000.tsp': 18659688}
    k_dict = {}
    min_k = []

    for g in distances:
        k_dict = {}
        min_k = []
        print(g)

        before = time.time()
        hk_tsp(1, g)
        after = time.time()
        print("Execution time: ", after - before)

        before = time.time()
        closest_insertion(g)
        after = time.time()
        print("Execution time: ", after - before)
        

        before = time.time()
        nearest_neighbor(g)
        after = time.time()
        print("Execution time: ", after - before)
        
        
        before = time.time()
        MST_Prim(g)
        after = time.time()
        print("Execution time: ", after - before)