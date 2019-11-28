import subprocess
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
import argparse
import utils

from student_utils import *
from tsp_solver.tsp_solver import tsp
"""
======================================================================
  Complete the following function.
======================================================================
"""

def plotGraph():
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_nodes(G, pos, node_color='c')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A list of (location, [homes]) representing drop-offs
    """
    t0 = time.perf_counter()

    # Create graph
    global G # Left here for debugging purposes
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)

    # Generate shortest path lengths to all nodes for dropoffs and returning to center
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)

    tsp_solution = tsp(list_of_locations, list_of_homes, starting_car_location, all_paths)
    tsp_solution = tsp_solution + [tsp_solution[0]]
    dropoffs = tsp_solution.copy()
    for iters in range(5):
        for i in range(1, len(dropoffs) - 1): #iterate from 1 to len-2
            min_j = -1;
            min_cost = float("inf")
            for j, _ in all_paths[tsp_solution[i]].items():
                cost = 2/3 * all_paths[j][dropoffs[i-1]] + all_paths[j][tsp_solution[i]] + 2/3 * all_paths[j][dropoffs[i+1]]
                if cost < min_cost:
                    min_cost = cost
                    min_j = j
            dropoffs[i] = min_j

    # Convert to format for saving
    listlocs, listdropoffs = [], {}
    for i in range(1, len(tsp_solution) - 1):
        if dropoffs[i] in listdropoffs:
            listdropoffs[dropoffs[i]].append(tsp_solution[i])
        else:
            listdropoffs[dropoffs[i]] = [tsp_solution[i]]

    listlocs = [dropoffs[0]]
    for i in range(1, len(dropoffs)):
        temp = []
        j = dropoffs[i-1]
        k = dropoffs[i]
        while (k != j):
            temp.insert(0, k)
            k = pcessors[j][k]
        listlocs.extend(temp)


    t1 = time.perf_counter() - t0
    print(" done! Time: {}s".format(t1))

    return listlocs, listdropoffs
                
"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing {}...'.format(input_file), end="")
    sys.stdout.flush()

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)


        
