# coding=utf-8


'''
Lab 2. La rete dei trasporti pubblici

Membri del gruppo: Alberto Bezzon, Tommaso Carraro e Alberto Gallinaro
'''

import os
from geopy.distance import geodesic  # for calculating coords distances
# import cPickle # saving graph to file
import math
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


# import numpy as np


#######################################################################################################################
class PriorityQueue:

    def __init__(self, l):
        '''
        Costruttore di oggetti PriorityQueue

        l: lista di dizionari (es {node: cost})
        '''
        self.queue = l
        self.build_heap()

    def left(self, i):
        '''
        Metodo che data la posizione di un nodo, restituisce la posizione del figlio sinistro
        all'interno della lista
        '''
        return 2 * i + 1

    def right(self, i):
        '''
        Metodo che data la posizione di un nodo, restituisce la posizione del figlio destro
        all'interno della lista
        '''
        return 2 * i + 2

    def parent(self, i):
        '''
        Metodo che data la posizione di un nodo, restituisce la posizione del padre
        all'interno della lista
        '''
        return math.floor((i - 1) / 2)

    def add(self, x):
        '''
        Metodo che aggiunge un nuovo nodo alla lista
        '''
        n = len(self.queue)
        self.queue.append(x)
        self.bubble_up(n)

    def bubble_up(self, i):
        '''
        Metodo riordina la lista in modo tale che le proprietà di una heap binaria
        siano rispettate
        '''
        p = self.parent(i)
        while i > 0 and list(self.queue[i].values())[0] < list(self.queue[p].values())[0]:
            aux = self.queue[i]
            self.queue[i] = self.queue[p]
            self.queue[p] = aux
            i = p
            p = self.parent(i)

    def decrease_key(self, i, x):
        '''
        Cambia il valore della chiave del nodo in posizione i con x
        '''
        for j in range(0, len(self.queue)):
            if list(self.queue[j].keys())[0] == str(i):
                if list(self.queue[j].values())[0] < x and not math.isinf(list(self.queue[j].values())[0]):
                    return False
                self.queue[j] = {i: x}
                self.bubble_up(j)
                return True
        return False

    def extract_min(self):
        '''
        Estrae il nodo con chiave minore nella lista
        '''
        min_ = self.queue[0]
        n = len(self.queue)
        self.queue[0] = self.queue[n - 1]
        del self.queue[-1:]
        self.trickle_down(0)
        return list(min_.keys())[0]

    def trickle_down(self, i):
        '''
        Ricostruisce l'heap binaria, facendo scendere il nodo in posizione i
        '''
        l = self.left(i)
        r = self.right(i)
        n = len(self.queue)
        smallest = i
        if l < n and list(self.queue[l].values())[0] < list(self.queue[i].values())[0]:
            smallest = l
        if r < n and list(self.queue[r].values())[0] < list(self.queue[smallest].values())[0]:
            smallest = r
        if smallest != i:
            aux = self.queue[i]
            self.queue[i] = self.queue[smallest]
            self.queue[smallest] = aux
            self.trickle_down(smallest)

    def build_heap(self):
        n = len(self.queue)
        for i in range(math.floor(n / 2) - 1, -1, -1):
            self.trickle_down(i)


#######################################################################################################################

# codice per la costruzione del grafo a partire dal dataset

path = "dataset/"
bahnhof_path = "dataset/bahnhof"
bfkoord_path = "dataset/bfkoord"
globalLons = []
globalLats = []


def remove_keys(list, dict):
    for k in list:
        if k in dict:
            del dict[k]


def create_graph():
    '''
    Legge le informazioni dai file e crea il grafo
    '''
    graph = dict()
    input_file = open(bahnhof_path, 'r')
    input_file.readline()
    for line in input_file:
        data = line.split()
        graph[data[0]] = {
            'name': " ".join(data[2:]),
            'coords': [],
            'arcs': []
        }

    input_file.close()
    input_file = open(bfkoord_path, 'r')
    input_file.readline()
    input_file.readline()
    for line in input_file:
        data = line.split()
        graph[data[0]]['coords'].append(data[1])
        graph[data[0]]['coords'].append(data[2])
        globalLons.append(float(data[1]))
        globalLats.append(float(data[2]))
    input_file.close()

    files = [f for f in os.listdir(path) if f.endswith('.LIN')]
    for f in files:
        input_file = open(path + f, 'r')
        previous, id_, name = "", "", ""
        start, arrive_time, start_time = "", "", ""
        for line in input_file:
            if (line[0] == '*' and line[1] == 'Z') or line[0] != '*':  # se sono sulla riga che inizia con *Z (nome linea) oppure su una linea senza asterisco (linea con orario)
                if line[0] == '*' and line[1] == 'Z':  # se sono sulla riga della linea
                    id_, name = line.split()[1:3]
                else:
                    start = line[0:9]
                    arrive_time = line[32:37]
                    start_time = line[39:44]
                    if arrive_time != "" and previous[0] != '*':
                        graph[previous[0:9]]['arcs'].append({
                            'arrive_station': start,
                            'start_time': previous[39:44],
                            'arrive_time': arrive_time,
                            'line': [id_, name]
                        })
                previous = line
        input_file.close()
        # rimozioni stazioni senza senso dal grafo
        to_remove = []
        for i in graph:
            if graph[i]['coords'] == []:
                to_remove.append(i)
        remove_keys(to_remove, graph)
    return graph


#######################################################################################################################

# codice che implementa l'algoritmo

def distance(a, b):
    '''
    Distanza tra due stazioni.
    Parametri:
        a, b: lista di due coordinate e.g: a = ['45.232342','67.423234']
    '''

    return geodesic(a, b).km


def euristic(graph, first_station, second_station):
    '''
    Valore dell'euristica dalla stazione 1 alla stazione 2. L'euristica restituisce il tempo di percorrenza del mezzo più
    veloce esistente in Belgio per percorrere la distanza in linea d'aria tra la stazione 1 e la stazione 2
    Il treno Thalsys è il treno più veloce in Belgio ed ha una velocità massima di 300 km/h
    :param first_station: stazione 1 (codice stazione ad esempio 008230082)
    :param second_station: stazione 2 (codice stazione)
    :return: tempo di percorrenza in minuti da parte del treno più veloce per percorrere la distanza in linea d'aria dalla stazione 1 alla stazione 2
    '''
    return (distance(graph[str(first_station)]['coords'], graph[str(second_station)]['coords']) / 300) * 60


def time_to_minutes(time):
    '''
    Converte un'orario in minuti
    :param time: stringa, formato '00830'
    :return: orario in input convertito in minuti, integer
    '''
    hour = int(time[0:3])
    minutes = int(time[3:5])
    return hour * 60 + minutes


# funzione di inizializzazione dei dizionari di supporto all'algoritmo
def init_sssp(start, G, d, pi, depart_time):
    for k in G:
        d[k] = math.inf
        pi[k] = {
            'current': None,
            'start_time': None,
            'arrival_time': None,
            'line': None,
            'long': None,
            'lat': None,
            'station_name': None
        }
    d[start] = depart_time


def reconstruct_path(pi, end_node, depart_time, g):
    '''
    Dato il nodo finale ricostruisce il percorso ottimo
    :param pi: dizionario dei padri
    :param end_node: nodo destinazione
    :param depart_time: orario di partenza
    :return: lista di nodi
    '''
    list = []
    i = end_node
    list.append({
            'current': end_node,
            'start_time': None,
            'arrival_time': None,
            'line': None,
            'long': float(g[end_node]['coords'][0]),
            'lat': float(g[end_node]['coords'][1]),
            'station_name': g[end_node]['name']
        })
    while i != 'None':
        list.append(pi[i])
        i = str(pi[i]['current'])
    return list[::-1], depart_time


def check_time(time1, time2):
    '''
    Controlla se time1 >= time2
    :return: true|false
    '''
    return time1 >= time2



def take_time(time):
    '''
    Estre un orario da una stringa
    '''
    return time[1:3] + ":" + time[3:5]


def convert_in_time(time):
    hour = math.floor(time / 60)
    minutes = time - hour * 60
    if minutes < 10:
        return str(hour) + ":0" + str(minutes)
    else:
        return str(hour) + ":" + str(minutes)


def print_solution(solution_list, depart_time):
    '''
    prints prettified output
    '''
    lines_list = []
    string_to_print = ""
    depart_station = solution_list[1]['current']
    arrival_station = solution_list[len(solution_list) - 1]['current']
    arrival_time = solution_list[len(solution_list) - 2]['arrival_time']
    string_to_print += "Viaggio da " + depart_station + " a " + arrival_station + "\n"
    string_to_print += "Orario di partenza " + convert_in_time(depart_time) + "\n"
    string_to_print += "Orario di arrivo " + convert_in_time(arrival_time) + "\n"
    first = True
    change_labels = []
    for i in range(1, len(solution_list)-1):
        if solution_list[i]['line'] not in lines_list:
            change_labels.append(solution_list[i]['station_name'])
            if not first:
                string_to_print += " a " + solution_list[i]['current'] + "\n"
                string_to_print += convert_in_time(solution_list[i]['start_time']) + " : corsa " + \
                                   solution_list[i]['line'][0] + " " + solution_list[i]['line'][1] + " da " + \
                                   solution_list[i]['current']
            else:
                string_to_print += convert_in_time(solution_list[i]['start_time']) + " : corsa " + \
                                   solution_list[i]['line'][0] + " " + solution_list[i]['line'][1] + " da " + \
                                   solution_list[i]['current']
        first = False
        lines_list.append(solution_list[i]['line'])
    string_to_print += " a " + arrival_station
    print(string_to_print)
    change_labels.append(solution_list[len(solution_list) - 1]['station_name'])
    lons = []
    lats = []
    labels = []
    for i in range(1, len(solution_list)):
        lons.append(solution_list[i]['long'])
        lats.append(solution_list[i]['lat'])
        labels.append(solution_list[i]['station_name'])
    min_long = min(lons) - 0.8
    max_long = max(lons) + 0.8
    min_lat = min(lats) - 0.8
    max_lat = max(lats) + 0.8
    cent_lat = (min_lat + max_lat) / 2
    cent_long = (min_long + max_long) / 2
    m = Basemap(llcrnrlon=min_long, llcrnrlat=min_lat, urcrnrlon=max_long, urcrnrlat=max_lat, resolution='h',
                projection='cass', lat_0=cent_lat, lon_0=cent_long)
    # m = Basemap(llcrnrlon=min_long, llcrnrlat=min_lat, urcrnrlon=max_long, urcrnrlat=max_lat, epsg = 4181)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral')
    m.drawmapboundary()
    # m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Physical_Map', xpixels=1500, verbose=True)
    x1, y1 = m(globalLons, globalLats)
    m.plot(x1, y1, 'bo', markersize=0.5)
    x, y = m(lons, lats)
    m.plot(x, y, 'o-', markersize=4, color='white')
    # m.bluemarble()

    for label, xpt, ypt in zip(labels, x, y):
        if label in change_labels:
            plt.text(xpt + 0.5, ypt, label, color='#FFF0A5', size=10)
        else:
            plt.text(xpt + 0.5, ypt, label, color='white', size=10)

    plt.show()


# start, finish: id della stazione,
def A_star(start, finish, depart_time, G):
    closedNodes = []
    openNodes = []
    openNodes.append(start)

    pi = {}  # dizionario che contiene per ogni nodo il precedente

    d = {}  # dizionario delle distanze, per ogni nodo la distanza dalla partenza in termini di minuti

    init_sssp(start, G, d, pi, depart_time)

    nodeList = []
    for k in G.keys():
        nodeList.append(
            {k: math.inf})  # inizialmente euristica infinita per tutti i nodi, verrà aggiornata durante l'algoritmo
    eu_cost = PriorityQueue(nodeList)  # setto tutti i valori dell'euristica a infinito

    # For the first node, that value is completely heuristic.
    eu_cost.decrease_key(start, euristic(G, start, finish))  # per il nodo start devo settare l'euristica corretta

    while openNodes:
        current = eu_cost.extract_min()

        if current == finish:
            return reconstruct_path(pi, finish, depart_time, G)

        openNodes.remove(current)
        closedNodes.append(current)

        # ciclo del giorno stesso
        for i in G[current]['arcs']:  # per ogni stazione collegata alla stazione corrente
            if i['arrive_station'] not in closedNodes:  # esamino il nodo solo se non è già stato chiuso
                if check_time(time_to_minutes(i['start_time']), d[current]):  # d[current] è il tempo dal quale voglio partire dalla stazione (nodo) in cui mi trovo. i['start_time'] è l'orario di partenza dalla stazione in cui mi trovo per giungere alla stazione il cui arco esaminato si connette
                    temp_time = time_to_minutes(i['arrive_time'])  # temp time è il tempo di arrivo alla stazione a cui l'arco è connesso convertito in minuti
                    if i['arrive_station'] not in openNodes:  # Se la stazione in cui arrivo non fa parte dei nodi aperti significa che sto esaminando una nuova stazione
                        openNodes.append(i['arrive_station'])
                    if temp_time < d[i['arrive_station']]:  # se il tempo in minuti in cui arrivo alla stazione è minore del tempo ottimo con cui sono riuscito ad arrivare alla stazione fino a questo momento, allora devo effettuare dei cambiamenti, il nuovo tempo deve diventare quello ottimo
                        d[i['arrive_station']] = temp_time  # il nuovo tempo diventa quello ottimo
                        pi[i['arrive_station']] = {  # il predecessore della stazione diventa il current
                            'current': current,  # stazione di partenza dell'arco
                            'start_time': time_to_minutes(i['start_time']),  # orario di partenza da current
                            'arrival_time': time_to_minutes(i['arrive_time']),
                        # orario di arrivo in i['arrive_station']
                            'line': i['line'],  # linea usata,
                            'long': float(G[current]['coords'][0]),
                            'lat': float(G[current]['coords'][1]),
                            'station_name': G[current]['name']
                        }
                        eu_cost.decrease_key(i['arrive_station'],
                                             d[i['arrive_station']] + euristic(G, i['arrive_station'],
                                                                               finish))  # per la stazione viene modificata l'euristica nella heap perché è diventata migliore rispetto ad altre soluzioni
        # ciclo del giorno successivo (è necessario guardare anche il giorno successivo)
        for i in G[current]['arcs']:  # per ogni stazione collegata alla stazione corrente
            if i['arrive_station'] not in closedNodes:  # esamino il nodo solo se non è già stato chiuso
                if check_time((time_to_minutes(i['start_time']) + 24 * 60), d[current]):  # d[current] è il tempo dal quale voglio partire dalla stazione (nodo) in cui mi trovo. i['start_time'] è l'orario di partenza dalla stazione in cui mi trovo per giungere alla stazione il cui arco esaminato si connette
                    temp_time = time_to_minutes(i['arrive_time']) + 24 * 60  # temp time è il tempo di arrivo alla stazione a cui l'arco è connesso convertito in minuti
                    if i['arrive_station'] not in openNodes:  # Se la stazione in cui arrivo non fa parte dei nodi aperti significa che sto esaminando una nuova stazione
                        openNodes.append(i['arrive_station'])
                    if temp_time < d[i['arrive_station']]:  # se il tempo in minuti in cui arrivo alla stazione è minore del tempo ottimo con cui sono riuscito ad arrivare alla stazione fino a questo momento, allora devo effettuare dei cambiamenti, il nuovo tempo deve diventare quello ottimo
                        d[i['arrive_station']] = temp_time  # il nuovo tempo diventa quello ottimo
                        pi[i['arrive_station']] = {  # il predecessore della stazione diventa il current
                            'current': current,  # stazione di partenza dell'arco
                            'start_time': time_to_minutes(i['start_time']) + 24 * 60,  # orario di partenza da current
                            'arrival_time': time_to_minutes(i['arrive_time']) + 24 * 60,
                        # orario di arrivo in i['arrive_station']
                            'line': i['line'],  # linea usata,
                            'long': float(G[current]['coords'][0]),
                            'lat': float(G[current]['coords'][1]),
                            'station_name': G[current]['name']
                        }
                        eu_cost.decrease_key(i['arrive_station'],
                                             d[i['arrive_station']] + euristic(G, i['arrive_station'],
                                                                               finish))  # per la stazione viene modificata l'euristica nella heap perché è diventata migliore rispetto ad altre soluzioni


g = create_graph()

lista, depart_time = A_star('500000079', '300000044', time_to_minutes('01300'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('200415016', '200405005', time_to_minutes('00930'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('300000032', '400000122', time_to_minutes('00530'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('210602003', '300000030', time_to_minutes('00630'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('200417051', '140701016', time_to_minutes('01200'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('200417051', '140701016', time_to_minutes('02355'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('120904001', '120103002', time_to_minutes('01055'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('150303001', '130107002', time_to_minutes('00755'), g)
print_solution(lista, depart_time)
lista, depart_time = A_star('300000032', '150104001', time_to_minutes('00320'), g)
print_solution(lista, depart_time)