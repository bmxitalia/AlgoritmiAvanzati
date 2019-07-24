import csv
import matplotlib.pyplot as plt

def plot_one():
    points = []
    serial_time = []
    parallel_time = []
    
    with open('questionOne.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                points.append(int(row[0]))
                serial_time.append(float(row[1]))
                parallel_time.append(float(row[2]))
        
    plt.xlabel("Numero di punti", fontSize=10)
    plt.ylabel("Tempo (s)", fontSize=10)
    plt.title("Domanda 1")
    plt.plot(points, serial_time, marker='', color='red', label = 'Seriale')
    plt.plot(points, parallel_time, marker='', color='blue', label = 'Parallelo')
    plt.legend(loc='upper left', prop={'size': 10})
    plt.show()

    # return points, serial_time, parallel_time


def plot_two():
    cluster = []
    serial_time = []
    parallel_time = []
    
    with open('questionTwo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                cluster.append(int(row[0]))
                serial_time.append(float(row[1]))
                parallel_time.append(float(row[2]))
        
    plt.xlabel("Numero di cluster", fontSize=10)
    plt.ylabel("Tempo (s)", fontSize=10)
    plt.title("Domanda 2")
    plt.plot(cluster, serial_time, marker='', color='red', label = 'Seriale')
    plt.plot(cluster, parallel_time, marker='', color='blue', label = 'Parallelo')
    plt.legend(loc='upper left', prop={'size': 10})
    plt.show()


def plot_three():
    iterations = []
    serial_time = []
    parallel_time = []
    
    with open('questionThree.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                iterations.append(int(row[0]))
                serial_time.append(float(row[1]))
                parallel_time.append(float(row[2]))
        
    plt.xlabel("Numero di iterazioni", fontSize=10)
    plt.ylabel("Tempo (s)", fontSize=10)
    plt.title("Domanda 3")
    plt.plot(iterations, serial_time, marker='', color='red', label = 'Seriale')
    plt.plot(iterations, parallel_time, marker='', color='blue', label = 'Parallelo')
    plt.legend(loc='upper left', prop={'size': 10})
    plt.show()


def plot_four():
    cutoffs = []
    time = []
    
    with open('questionFour.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                cutoffs.append(int(row[0]))
                time.append(float(row[1]))
        
    plt.xlabel("Cutoff", fontSize=10)
    plt.ylabel("Tempo (s)", fontSize=10)
    plt.title("Domanda 4")
    plt.plot(cutoffs, time, marker='', color='red')
    plt.show()

if __name__ == "__main__":
    plot_one()
    plot_two()
    plot_three()
    plot_four()

