import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
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

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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

    # TODO convert this to use numbers and not names

    t0 = time.perf_counter()

    class Car():
        def __init__(self, loc, tas, reached):
            self.loc = loc
            self.tas = tas.copy()
            self.reached = reached.copy() # if already reached/left a place, can't dropoff there anymore, doesn't necessarily include current location

        def __eq__(self, other):
            return self.loc == other.loc and self.tas == other.tas # don't need reached

        def __hash__(self):
            return hash(self.loc) + sum([hash(l) for l in self.tas])

        def __str__(self):
            return "Car({}, {}, {})".format(self.loc, self.tas, self.reached)

        def __repr__(self):
            return self.__str__()

        def isDone(self):
            return self.loc == starting_car_location and len(self.tas) == 0

    # Create graph
    global G # TODO remove this line
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)

    # Convert locations to indices
    list_of_homes = set([list_of_locations.index(h) for h in list_of_homes])
    starting_car_location = list_of_locations.index(starting_car_location)

    # Generate shortest path lengths to all nodes for dropoffs and returning to center
    all_paths = dict(nx.all_pairs_dijkstra_path_length(G))

    # Initialize variables for Dijkstra's
    pq = hd.heapdict()
    startcar = Car(starting_car_location, list_of_homes.copy(), set())
    paths, costs = {}, {}

    # Add source point
    pq[startcar] = 0
    paths[startcar] = None
    costs[startcar] = 0

    # Code drops off TAs and moves, this is edge case where we drop off everyone and then move
    endcar = Car(starting_car_location, set(), set())
    naivecost = sum([all_paths[starting_car_location][t] for t in list_of_homes])
    pq[endcar] = naivecost
    paths[endcar] = startcar
    costs[endcar] = naivecost

    inf = float('inf')

    # Run Dijkstra's
    while pq:
        # Pop off smallest in PQ
        car, currcost = pq.popitem()

        if car.isDone():
            break

        if car.loc in car.reached: # If we've been here before, can't drop off here bc we could've done it earlier (and have)
            for n in G.neighbors(car.loc):
                newcost = currcost + 2/3 * all_paths[car.loc][n]
                newcar = Car(n, car.tas, car.reached)
                oldcost = costs.setdefault(newcar, inf)
                # Relax edge
                if newcost < oldcost:
                    pq[newcar] = newcost
                    costs[newcar] = newcost
                    paths[newcar] = car
        else:
            tas = car.tas - {car.loc} # if at home, drop them off
            poss_dps = [set(pd) for pd in powerset(tas)] # ways to have people left in car
            poss_dps_costs = [sum([all_paths[car.loc][t] for t in (tas - pd)]) for pd in poss_dps] # generate costs for each dropoff
            newreached = car.reached.union(set([car.loc]))
            for n in G.neighbors(car.loc):
                for pd, pdcost in zip(poss_dps, poss_dps_costs):
                    newcost = currcost + pdcost + 2/3 * all_paths[car.loc][n]
                    newcar = Car(n, pd, newreached)
                    oldcost = costs.setdefault(newcar, inf)
                    # Relax edge
                    if newcost < oldcost:
                        pq[newcar] = newcost
                        costs[newcar] = newcost
                        paths[newcar] = car

    minpath = []
    currcar = Car(starting_car_location, set(), set())
    minpath.append(currcar)
    while currcar != startcar:
        currcar = paths[currcar]
        minpath.append(currcar)
    minpath = minpath[::-1]
    

    listlocs, listdropoffs = [], {}
    for i in range(len(minpath)):
        listlocs.append(minpath[i].loc)
        if (i < len(minpath) - 1):
            drops = minpath[i].tas - minpath[i+1].tas
            if len(drops) > 0:
                listdropoffs[minpath[i].loc] = list(drops)

    # naive case
    if len(listlocs) == 2:
        listlocs = listlocs[:1]

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
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
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


        
