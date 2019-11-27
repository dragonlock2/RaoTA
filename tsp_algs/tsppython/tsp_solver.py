import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('/opt/localsolver_9_0/bin/python37')
import localsolver
import os
import subprocess
import argparse
import utils

from student_utils import *

input_file = "libs/inputs/15.in"
with localsolver.LocalSolver() as ls:
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)

    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)
    important_locations = [list_locations.index(starting_car_location)] + [list_locations.index(i) for i in list_houses]
    print(list_locations)
    print('asdf')
    print(starting_car_location)
    print('asdf')
    print(list_houses)
    print('asdf')
    print(important_locations)

    # Distance from i to j
    distance_weight = [[int(all_paths[i][j]) for i in important_locations] for j in important_locations]

    #
    # Declares the optimization model
    #
    model = ls.model

    # A list variable: cities[i] is the index of the ith city in the tour
    cities = model.list(len(important_locations)) 
    # All cities must be visited
    model.constraint(model.count(cities) == len(important_locations))

    # Create a LocalSolver array for the distance matrix in order to be able to 
    # access it with "at" operators.
    distance_array = model.array(distance_weight)

    # Minimize the total distance
    dist_selector = model.function(lambda i: model.at(distance_array, cities[i-1], cities[i]))
    obj = (model.sum(model.range(1, len(important_locations)), dist_selector)
            + model.at(distance_array, cities[len(important_locations) - 1], cities[0]));
    model.minimize(obj)

    model.close()

    #
    # Parameterizes the solver with a time limit in seconds
    #
    ls.param.time_limit = 20

    # Solve
    ls.solve()

    #
    # Writes the solution in a file
    #
    with open('tsp_test.out', 'w') as f:
        f.write("%d\n" % obj.value)
        for c in cities.value:
            f.write("%d " % c)
        f.write("\n")
        for c in cities.value:
            f.write("%s " % list_locations[important_locations[c]])
        f.write("\n")
