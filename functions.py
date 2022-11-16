import random
#import time
import matplotlib.pyplot as plt


def distanceTable(input_data):
    cities_count = input_data[0]
    cities_coordinate = input_data[1:]
    d_table = [[0 for _ in range(cities_count)] for __ in range(cities_count)]
    for i in range(1, cities_count + 1):
        for j in range(1, cities_count + 1):
            if i == j:
                continue
            cityA = input_data[i]
            cityB = input_data[j]
            d_table[i-1][j-1] = round((((cityA[0] - cityB[0])**2 +
                                        (cityA[1] - cityB[1])**2 + (cityA[2] - cityB[2])**2) ** 0.5), 2)

    return cities_count, cities_coordinate, d_table


def initialPopulation(cities_size, population_size):
    population = []
    tmp = [i for i in range(cities_size)]
    for i in range(population_size):
        order = tmp[::]
        random.shuffle(order)
        population.append(order)

    return population


def calcFitness(orders, d_table, bestEver, bestOrder):
    fitness = []
    curBest = float('inf')
    curBestOrder = []
    for order in orders:
        d = 0
        for i in range(len(order) - 1):
            city1 = order[i]
            city2 = order[i + 1]
            d += d_table[city1][city2]
        d += d_table[order[-1]][order[0]]
        if d < bestEver:
            bestEver = d
            bestOrder = order
        if d < curBest:
            curBestOrder = order
        fitness.append(1 / (d + 1))

    total = sum(fitness)
    for i in range(len(fitness)):
        fitness[i] = fitness[i] / total * 100

    return fitness, bestEver, bestOrder, curBestOrder


def selection(pupolation, fitness, pool_size):
    # K-way tourament
    indice = [i for i in range(len(pupolation))]
    selection_pool = []
    for i in range(pool_size):
        index_pool = random.choices(indice, k=10)
        index_dict = {fitness[index_pool[i]]: index_pool[i]
                      for i in range(len(index_pool))}
        index = index_dict[max(fitness[index_pool[i]]
                               for i in range(len(index_pool)))]
        selection_pool.append(pupolation[index])

    return selection_pool


def crossOver(selection_pool, population_size):
    new_population = []
    # OX(1)
    for i in range(population_size):
        orderA, orderB = random.choices(
            selection_pool, k=2)

        start = random.randint(0, len(orderA) - 2)
        end = random.randint(start+1, len(orderA) - 1)
        new_order = ['#' for _ in range(len(orderA))]
        new_order[start:end + 1] = orderA[start:end + 1]
        for i in range(len(new_order)):
            N = len(orderA)
            while orderB[start] in new_order and '#' in new_order:
                start = (start + 1) % len(new_order)
            if new_order[i] != '#':
                continue
            new_order[i] = orderB[start]
            start = (start + 1) % len(new_order)
        new_population.append(new_order)
    return new_population


def mutate(orders, rate):
    for order in orders:
        # Swap
        if random.random() < rate:
            indexA = random.randint(0, len(order) - 1)
            indexB = random.randint(0, len(order) - 1)
            order[indexA], order[indexB] = order[indexB], order[indexA]
        # Scamble
        if random.random() < rate:
            indexA = random.randint(0, len(order) - 2)
            indexB = random.randint(indexA+1, len(order) - 1)
            sub_list = order[indexA:indexB + 1]
            random.shuffle(sub_list)
            order[indexA:indexB + 1] = sub_list
        # Reverse
        if random.random() < rate:
            indexA = random.randint(0, len(order) - 2)
            indexB = random.randint(indexA+1, len(order) - 1)
            sub_list = order[indexA:indexB + 1]
            sub_list.reverse()
            order[indexA:indexB + 1] = sub_list

    return orders


def outputTxt(bestOrder, coordinate):
    with open('output.txt', 'w') as f:
        for i in bestOrder:
            coord = coordinate[i]
            line = " ".join(str(c) for c in coord)
            f.write(line)
            f.write('\n')
        line = " ".join(str(c) for c in coordinate[bestOrder[0]])
        f.write(line)
    f.close()


def draw(coords, curBest, best):
    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x_coords = []
    y_coords = []
    z_coords = []
    for x, y, z in coords:
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)

    line_x = []
    line_y = []
    line_z = []
    for i in curBest:
        line_x.append(x_coords[i])
        line_y.append(y_coords[i])
        line_z.append(z_coords[i])

    best_x = []
    best_y = []
    best_z = []
    for i in best:
        best_x.append(x_coords[i])
        best_y.append(y_coords[i])
        best_z.append(z_coords[i])

    ax.plot(x_coords, y_coords, z_coords, 'ob')
    ax.plot(line_x, line_y, line_z, ':r')
    ax.plot(best_x, best_y, best_z)
    plt.show()
    plt.pause(0.001)
    plt.close()

    return
