import os
import sys
import subprocess
sys.path.append('libs')
import argparse
import utils
import brute

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

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
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)

    # Convert locations to indices
    list_of_homes = set([list_of_locations.index(h) for h in list_of_homes])
    starting_car_location = list_of_locations.index(starting_car_location)

    # Generate shortest path lengths to all nodes for dropoffs and returning to center
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)

    # Get existing output solution
    outfile = "outputs/" + os.path.splitext(os.path.basename(params[0]))[0] + ".out"
    f = open(outfile)
    listlocs = f.readline().strip().split(" ")
    listlocs = [list_of_locations.index(h) for h in listlocs]
    listdropoffs = {}
    for i in range(int(f.readline())):
        dp = [list_of_locations.index(h) for h in f.readline().strip().split(" ")]
        listdropoffs[dp[0]] = dp[1:]
    f.close()

    # Convert to better form
    dropcycle = [(i, []) for i in listlocs]
    for key in listdropoffs:
        dropcycle[listlocs.index(key)][1].extend(listdropoffs[key])

    # Check if TAs share a path home
    insertions = []
    for c in dropcycle:
        d = {n:[] for n in G.neighbors(c[0])}
        for t in c[1]:
            if t != c[0]:
                d[pcessors[t][c[0]]].append(t)
        groups = [d[key] for key in d if len(d[key]) > 1]
        insert = []
        if groups:
            insert.append((c[0], list(set(c[1]) - set().union(*groups)))) # dropoff everyone who walks alone
            for g in groups:
                ll, ld = brute.solve(c[0], set(g), G, pcessors, all_paths) # brute force to determine optimal dropoff of rest of guys
                

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
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=[input_file])

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
