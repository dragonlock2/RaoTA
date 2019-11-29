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

## TSP solver
# Returns an ordered list of indicies of the adjacency_matrix starting with the starting_car_location
def tsp(list_locations, list_houses, starting_car_location, all_paths, timeout=5):
    with localsolver.LocalSolver() as ls:

        important_locations = [list_locations.index(starting_car_location)] + [list_locations.index(i) for i in list_houses]
        
        # print(list_locations)
        # print('asdf')
        # print(starting_car_location)
        # print('asdf')
        # print(list_houses)
        # print('asdf')
        # print(important_locations)

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
        ls.param.time_limit = timeout

        # Solve
        ls.solve()

        # Reorder solution so starting_car_location is first
        scl_i = -1
        for i in range(cities.value.count()):
            if list_locations[important_locations[cities.value.get(i)]] == starting_car_location:
                scl_i = i
                break
        if scl_i == -1:
            raise Exception('Could not determine starting car location in TSP solution\n')
        tsp_solution = [important_locations[cities.value.get((scl_i + i) % cities.value.count())] for i in range(cities.value.count())]

        return tsp_solution

if __name__ == "__main__":
    input_file = "libs/inputs/15.in"
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)
    print(pcessors)
    tsp_sol = tsp(list_locations, list_houses, starting_car_location, all_paths)
    #
    # Writes the solution in a file
    #
    with open('tsp_test.out', 'w') as f:
        for item in tsp_sol:
            f.write("%s " % list_locations[item])
        f.write("\n")
