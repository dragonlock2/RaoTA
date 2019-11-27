import localsolver
import sys
import os
import subprocess
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *

input_file = "asdfasdf.in"
with localsolver.LocalSolver() as ls:
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)

    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)
    

    # Distance from i to j
    distance_weight = [[int(next(file_it)) for i in range(nb_cities)] for j in range(nb_cities)] 

    #
    # Declares the optimization model
    #
    model = ls.model

    # A list variable: cities[i] is the index of the ith city in the tour
    cities = model.list(nb_cities) 

    # All cities must be visited
    model.constraint(model.count(cities) == nb_cities)

    # Create a LocalSolver array for the distance matrix in order to be able to 
    # access it with "at" operators.
    distance_array = model.array(distance_weight)

    # Minimize the total distance
    dist_selector = model.function(lambda i: model.at(distance_array, cities[i-1], cities[i]))
    obj = (model.sum(model.range(1, nb_cities), dist_selector)
            + model.at(distance_array, cities[nb_cities - 1], cities[0]));
    model.minimize(obj)

    model.close()

    #
    # Parameterizes the solver
    #
    if len(sys.argv) >= 4: ls.param.time_limit = int(sys.argv[3])
    else: ls.param.time_limit = 5

    ls.solve()

    #
    # Writes the solution in a file
    #
    if len(sys.argv) >= 3:
        # Writes the solution in a file 
        with open(sys.argv[2], 'w') as f:
            f.write("%d\n" % obj.value)
            for c in cities.value:
                f.write("%d " % c)
            f.write("\n")
