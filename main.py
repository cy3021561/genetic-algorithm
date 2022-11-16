from time import process_time
import functions
#import numpy as np

# Initialize data
start_time = process_time()
input_data = []
with open('input.txt', 'r') as f:

    for i, line in enumerate(f):
        if i == 0:
            input_data.append(int(line))
        else:
            line_split = line.split(" ")
            input_data.append([int(line_split[0]),
                               int(line_split[1]), int(line_split[2])])
f.close()
cities_size, coordinate, d_table = functions.distanceTable(input_data)
# print(coordinate)
# for i in range(cities):
#     print(i, d_table[i])

# Population
POPULATION_SIZE = 1000
MUTATION_RATE = 0.1
POOL_SIZE = 100
bestEver = float('inf')
bestOrder = None
population = functions.initialPopulation(cities_size, POPULATION_SIZE)
program_time = 1000
if cities_size >= 100:
    program_time = 70
if cities_size >= 200:
    program_time = 95
if cities_size >= 400:
    program_time = 195


# GA algorithm
while process_time() < program_time:
    #process_time = cur_time - start_time
    fitness, bestEver, bestOrder, curBestOrder = functions.calcFitness(
        population, d_table, bestEver, bestOrder)
    selection_pool = functions.selection(population, fitness, POOL_SIZE)
    new_population = functions.crossOver(selection_pool, POPULATION_SIZE)
    population = functions.mutate(new_population, MUTATION_RATE)
    functions.draw(coordinate, curBestOrder, bestOrder)
functions.outputTxt(bestOrder, coordinate)
