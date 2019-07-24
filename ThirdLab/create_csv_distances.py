import os
import math
import copy
import csv

RRR = 6378.388
distances = {}
list_graphs = []


def create_graph():
    path = "dataset/"
    graphs = {}

    files = [f for f in os.listdir(path) if f.endswith('.tsp')]
    for f in files:
        input_file = open(path + f, 'r')
        encode_type = ""
        line = input_file.readline()

        # find type of encoding
        while 'EDGE_WEIGHT_TYPE' not in line:
            line = input_file.readline()

        data = line.split(':')
        encode_type = data[1].replace(" ", "")[0:len(encode_type) - 1]
        graph = {
            'type': encode_type,
            'points': {}
        }

        # find the beginning of relevant data
        while line != 'NODE_COORD_SECTION\n':
            line = input_file.readline()

        for line in input_file:
            if line != 'EOF\n':
                data = line.split()

                # somehow the split fails at the end
                if len(data) > 0:
                    x = float(data[1])
                    y = float(data[2])
                    if encode_type == "GEO":
                        x = convert_to_radiant(x)  # latitude
                        y = convert_to_radiant(y)  # longitude
                    graph['points'][int(data[0])] = [x, y]
        graphs[f] = copy.deepcopy(graph)
        list_graphs.append(copy.deepcopy(graph))
    return graphs


def convert_to_radiant(value):
    deg = int(value)
    min_ = value - deg
    return math.pi * (deg + 5.0 * min_ / 3.0) / 180.0


def distance(v1, v2, graph):
    x1 = graph['points'][v1][0]
    y1 = graph['points'][v1][1]
    x2 = graph['points'][v2][0]
    y2 = graph['points'][v2][1]
    if graph['type'] == "GEO":
        q1 = math.cos(y1 - y2)  # compute longitude
        q2 = math.cos(x1 - x2)  # compute latitude
        q3 = math.cos(x1 + x2)
        return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
    else:
        return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))


def create_csv(graphs):
    count_g = 0
    for graph in graphs:
        distances[graph] = {}
        for i in graphs[graph]['points']:
            for j in graphs[graph]['points']:
                if i != j:
                    key = str(i)+"|"+str(j)
                    distances[graph][key] = distance(i, j, list_graphs[count_g])
        count_g += 1

    with open('distances.csv', mode='w', newline='') as csv_file:
        fieldnames = ['graph', 'key', 'distance']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for graph in distances:
            for key in distances[graph]:
                writer.writerow({'graph': graph, 'key': key, 'distance': distances[graph][key]})


g = create_graph()
create_csv(g)
