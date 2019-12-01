import os
import sys
import subprocess
sys.path.append('libs')
import argparse
import utils
import brute

# Run in python3.7 (for now)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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
        if groups:
            insert = [(c[0], list(set(c[1]) - set().union(*groups)))] # dropoff everyone who walks alone
            for g in groups:
                lilo, lidr = brute.solve(c[0], set(g), G, pcessors, all_paths) # brute force to determine optimal dropoff of rest of guys
                for li in lilo[1:]: # don't include first one bc we know it
                    if li in lidr:
                        insert.append((li, lidr[li]))
                    else:
                        insert.append((li, []))
            insertions.append(insert)

    listinsertionpoints = [i[0][0] for i in insertions]
    newdc = []
    for i in dropcycle:
        if i[0] in listinsertionpoints and len(i[1]) > 0:
            index = -1
            for j in range(len(insertions)):
                if insertions[j][0][0] == i[0]:
                    index = j
                    break
            newdc.extend(insertions[index])
        else:
            newdc.append(i)
    dropcycle = newdc

    # Update listlocs and listdropoffs
    listlocs = [i[0] for i in dropcycle]
    listdropoffs = {i[0]:i[1] for i in dropcycle if len(i[1]) > 0}
    listdropoffs = {}
    for i in dropcycle:
        if len(i[1]) > 0:
            if i[0] in listdropoffs:
                listdropoffs[i[0]].extend(i[1])
            else:
                listdropoffs[i[0]] = i[1]

    # Run TSP to get a better cycle
    listdps = list(listdropoffs.keys()) # contains all points that must be gone through
    if starting_car_location not in listdps:
        listdps.append(starting_car_location)

    dpmap = {i:listdps[i] for i in range(len(listdps))}
    data_dist = [[0 for _ in range(len(dpmap))] for _ in range(len(dpmap))]
    for i in range(len(data_dist)):
        for j in range(len(data_dist)):
            data_dist[i][j] = int(all_paths[dpmap[i]][dpmap[j]]*1000000) # OR tools only uses integers
    data_num_vehicles = 1
    data_depot = -1 # starting location
    for key in dpmap:
        if dpmap[key] == starting_car_location:
            data_depot = key
            break

    manager = pywrapcp.RoutingIndexManager(len(data_dist), data_num_vehicles, data_depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data_dist[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 5 # CHANGE THIS
    assignment = routing.SolveWithParameters(search_parameters)
    if not assignment:
        raise Exception("Nani TSP didn't work!")

    newcycle = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        newcycle.append(manager.IndexToNode(index))
        index = assignment.Value(routing.NextVar(index))
    newcycle.append(manager.IndexToNode(index))
    newcycle = [dpmap[i] for i in newcycle]

    # Update listlocs
    listlocs = []
    curr = -1
    for i in range(len(newcycle)-1):
        curr = newcycle[i]
        while curr != newcycle[i+1]:
            listlocs.append(curr)
            curr = pcessors[newcycle[i+1]][curr]
    listlocs.append(curr)

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
