import csv
import os
import copy
import sys
import math
import matplotlib.pyplot as plt
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)

# ritorna il grafo delle contee sottoforma di dizionario, la chiave e' il codice della contea, ogni chiave contiene le
# coordinate geografiche, la densita' demografica e il rischio di cancro.
# Inoltre ritorna una lista dei codici delle contee.
def create_graph():
    path = "dataset/"
    graphs = []
    P = []

    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    for f in files:
        graph = {}
        p = []
        with open(path+f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                p.append(row[0])
                graph[row[0]] = {
                    'coords': [row[1], row[2]],
                    'population': row[3],
                    'risk': row[4]
                }
        graphs.append(graph)
        P.append(p)
    return graphs, P


##################################### K-MEANS CLUSTERING ##############################################################

def insert_in_nearest_cluster(g, item, clusters):
    min = sys.maxsize
    nearest = -1
    x = float(g[item]['coords'][0])
    y = float(g[item]['coords'][1])
    for i in clusters:
        centroid_x = float(clusters[i]['centroid'][0])
        centroid_y = float(clusters[i]['centroid'][1])
        dist = math.sqrt((x - centroid_x) ** 2 + (y - centroid_y) ** 2) # calcolo distanza euclidea tra il punto e il centroide
        if dist < min:
            min = dist
            nearest = i
    clusters[nearest]['items'].append(item)

def compute_new_centroids(clusters, g):
    for cluster in clusters:
        sum_x = 0
        sum_y = 0
        for c in clusters[cluster]['items']:
            sum_x += float(g[c]['coords'][0])
            sum_y += float(g[c]['coords'][1])
        centroid_x = sum_x/len(clusters[cluster]['items'])
        centroid_y = sum_y/len(clusters[cluster]['items'])
        clusters[cluster]['centroid'] = [centroid_x, centroid_y]

def make_empty_clusters(clusters):
    for cluster in clusters:
        clusters[cluster]['items'] = []

def take_max(g):
    max = -sys.maxsize
    ret = -1
    for k in g:
        if int(g[k]['population']) > max:
            max = int(g[k]['population'])
            ret = k
    return ret

def k_means(g, k, q):
    clusters = {}
    temp_g = copy.deepcopy(g) # serve ad evitare il rischio di estrarre lo stesso elemento due volte, in questo modo i centroidi saranno tutti diversi
    for i in range(0, k):
        key = take_max(temp_g)
        del temp_g[key]
        clusters[i] = {
            'items': [],
            'centroid': [g[key]['coords'][0], g[key]['coords'][1]]
        }
    for i in range(0, q):
        make_empty_clusters(clusters)
        for j in list(g.keys()):
            insert_in_nearest_cluster(g, j, clusters)
        compute_new_centroids(clusters, g)
    return clusters
    

####################### HIERARCHICAL CLUSTERING ##########################################

def split(S, Pl, Pr):  # split corretto
    Sl = []
    Sr = []
    for i in range(0, len(S)):
        if S[i] in Pl:
            Sl.append(S[i])
        else:
            Sr.append(S[i])
    return Sl, Sr


def closestPairStrip(S, mid, d, G):  # funzione corretta
    n = len(S)
    S_prim = []
    for i in range(0, n):
        if abs(float(G[S[i]][0]) - mid) < d:
            S_prim.append(S[i])

    d, i, j = math.inf, -1, -1
    k = len(S_prim)

    for u in range(0, k - 1):
        for v in range(u + 1, min(u + 6, k)):
            tmp_dist = math.sqrt((float(G[S_prim[u]][0]) - float(G[S_prim[v]][0])) ** 2 + (float(G[S_prim[u]][1]) - float(G[S_prim[v]][1])) ** 2)
            if tmp_dist < d:
                d = tmp_dist
                i = S_prim[u]
                j = S_prim[v]

    return d, i, j

# P = ['123','123123','123123']
def slowestClosestPair(P, G):  # funzione corretta
    d, i, j = math.inf, -1, -1 
    for u in P:
        for v in P:
            if v != u:
                tmp_dist = math.sqrt((float(G[u][0]) - float(G[v][0])) ** 2 + (float(G[u][1]) - float(G[v][1])) ** 2)
                if tmp_dist < d:
                    d = tmp_dist
                    i = u
                    j = v
    return d, i, j


def fastClosestPair(P, S, G):  # funzione corretta
    n = len(P)
    if n <= 3:
        return slowestClosestPair(P, G)
    else:
        m = math.floor(n/2)
        Pl = P[:m]
        Pr = P[m:n]
        Sl, Sr = split(S, Pl, Pr)

        d1, i1, j1 = fastClosestPair(Pl, Sl, G)
        d2, i2, j2 = fastClosestPair(Pr, Sr, G)

        if d1 < d2:
            d = d1
            i = i1
            j = j1
        else:
            d = d2
            i = i2
            j = j2

        mid = (float(G[P[m - 1]][0]) + float(G[P[m]][0])) / 2
        dc, ic, jc = closestPairStrip(S, mid, d, G)
        if dc < d:
            return dc, ic, jc
        else:
            return d, i, j

def compute_new_centroid(items, G):
    sum_x = 0
    sum_y = 0
    for i in items:
        sum_x += float(G[i]['coords'][0])
        sum_y += float(G[i]['coords'][1])
    return [sum_x/len(items), sum_y/len(items)]

def hierarirchical_clustering(P, G, k):
    centroidDict = {}
    clusters = {}
    centroids = []
    centroidsY = []
    for i in range(0, len(P)):
        clusters[i] = {
            'items': [P[i]],  # ogni cluster contiene inizialmente un punto
            'centroid': G[P[i]]['coords']  # il centroide del cluster corrisponde alle coordinate dell'unico punto
        }
        centroidDict[i] = G[P[i]]['coords']
        centroids.append(i)
        centroidsY.append(i)
    while len(clusters) > k:
        # ordinamento centroidi per coordinata x e y crescente
        mergeSort(centroids, centroidDict, 0)
        mergeSort(centroidsY, centroidDict, 1)
        # trovo i centroidi più vicini e la loro distanza
        d, i, j = fastClosestPair(centroids, centroidsY, centroidDict) # ho i centroidi piu' vicini
        # i e j sono i centroidi più vicini. Mergio i cluster in i ed elimino j
        new_index = 0
        while new_index in clusters:
            new_index = new_index + 1
        pointsi = clusters.pop(i)['items'] # rimuovo il cluster i
        pointsj = clusters.pop(j)['items'] # rimuovo il cluster j
        clusters[new_index] = { # creo un nuovo cluster che contiene i precedenti due
            'items': [],
            'centroid': []
        }
        for point in pointsi:
            clusters[new_index]['items'].append(point)
        for point in pointsj:
            clusters[new_index]['items'].append(point)
        centroids.remove(j)
        centroidsY.remove(j)
        centroidsY.remove(i)
        centroids.remove(i)
        centroidDict.pop(j)
        centroidDict.pop(i)
        centroidsY.append(new_index)
        centroids.append(new_index)
        clusters[new_index]['centroid'] = compute_new_centroid(clusters[new_index]['items'], G)
        centroidDict[new_index] = clusters[new_index]['centroid']
    return clusters


def mergeSort(arr, G, coord):  # merge sort utilizzato per ordinare gli array in maniera efficiente
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        mergeSort(L, G, coord)  # Sorting the first half
        mergeSort(R, G, coord)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if float(G[L[i]][coord]) < float(G[R[j]][coord]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


########################## CALCOLO DISTORSIONE #######################################################################

def error_metric(clusters, G):
    errors = {}

    for cluster in list(clusters.keys()):
        acc = 0
        errors[cluster] = 0

        for node in clusters[cluster]['items']:
            acc += math.sqrt((float(G[node]['coords'][0]) - float(clusters[cluster]['centroid'][0])) ** 2 + (float(G[node]['coords'][1]) - float(clusters[cluster]['centroid'][1])) ** 2) ** 2 * float(G[node]['population'])

        errors[cluster] = acc
    
    return errors

def distortion_metric(errors):
    acc = 0
    for err in list(errors.keys()):
        acc += errors[err]

    return acc

################################## STAMPA RISULTATI ###################################################################

def draw(clusters, g):
    LABEL_COLOR_MAP = {0: '#e6194b',
                       1: '#3cb44b',
                       2: '#ffe119',
                       3: '#4363d8',
                       4: '#f58231',
                       5: '#911eb4',
                       6: '#46f0f0',
                       7: '#f032e6',
                       8: '#bcf60c',
                       9: '#fabebe',
                       10: '#008080',
                       11: '#ffffff',
                       12: '#9a6324',
                       13: '#fffac8',
                       14: '#800000',
                       15: '#aaffc3',
                       16: '#808000',
                       17: '#ffd8b1',
                       18: '#000075',
                       19: '#808080',
                       20: '#e6beff'
                    }

    im = plt.imread('USA_Counties.png')
    implot = plt.imshow(im, zorder=0)
    count = 0
    centroid_x = []
    centroid_y = []
    for cluster in clusters:
        x = []
        y = []
        for point in clusters[cluster]['items']:
            x.append(float(g[point]['coords'][0]))
            y.append(float(g[point]['coords'][1]))
            plt.plot([float(g[point]['coords'][0]), clusters[cluster]['centroid'][0]], [float(g[point]['coords'][1]), clusters[cluster]['centroid'][1]], c=LABEL_COLOR_MAP[count], linewidth=0.3, zorder=5)
        if float(x[0]) == float(clusters[cluster]['centroid'][0]):
            centroid_x.append(x[0])
            centroid_y.append(y[0])
        else:
            plt.scatter(x, y, marker='o', s=[3], c=LABEL_COLOR_MAP[count], zorder=5)
            plt.scatter(clusters[cluster]['centroid'][0], clusters[cluster]['centroid'][1], marker='*', s=[30], c='black', zorder=10)
        count += 1
    plt.scatter(centroid_x, centroid_y, marker='*', s=[30], c='black', zorder=10)
    plt.box(False)
    plt.axis('off')
    plt.show()

#######################################################################################################################

# Il main esegue il codice per rispondere alla domanda 9. Esegue i metodi di clustering k-means e gerarchico su tutti e
# 4 i dataset. Vengono testati un numero di cluster tra 6 e 20 su tutti e 4 i dataset. Per ogni clustering generato
# viene visualizzata la mappa del clustering e il tempo necessario per l'esecuzione del clustering.
if __name__ == '__main__':
    G, P = create_graph()
    i = 0
    distorsions = {}
    for g in G:
        distorsions[len(g.keys())] = {}
        xs = []
        yk = []
        yh = []
        for n_cluster in range(6, 21):

            before = time.time()
            clusters = k_means(g, n_cluster, 5)
            draw(clusters, g)
            error_k = error_metric(clusters, g)
            distorsion_k = distortion_metric(error_k)


            # print("=======================================================================================================")
            print("k-means |  data:", len(g.keys()), "\tdistorsion:", distorsion_k, "\tclusters:", n_cluster, "\ttime:", time.time()-before)
            # print("=======================================================================================================")

            #plt.scatter(n_cluster, distorsion_k, c=0)
            xs.append(n_cluster)
            yk.append(distorsion_k)

            before = time.time()

            c = hierarirchical_clustering(P[i], g, n_cluster)
            draw(c, g)
            errors_h = error_metric(c, g)
            distorsion_h = distortion_metric(errors_h)

            # print("=======================================================================================================")
            print("hierarc |  data:", len(g.keys()),  "\tdistorsion:", distorsion_h, "\tclusters:",n_cluster, "\ttime:", time.time()-before)
            # print("=======================================================================================================")

            yh.append(distorsion_h)

            after = time.time()



        plt.xlabel("Numero di cluster", fontSize=16)
        plt.ylabel("Distorsione", fontSize=16)
        plt.title("Numero contee:" + str(len(g.keys())))
        plt.scatter(xs, yk, label='k-means', c='firebrick')
        plt.plot(xs, yk,  c='firebrick')
        plt.scatter(xs, yh, label='gerarchico', c='royalblue')
        plt.plot(xs, yh, c='royalblue')
        plt.legend(loc='upper right', prop={'size': 20})
        plt.show()
        plt.clf()
        i += 1