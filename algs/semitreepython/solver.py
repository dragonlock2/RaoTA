import os
import sys
import subprocess
sys.path.append('libs')
sys.path.append('algs/optimizedtsp')
import argparse
import utils
import brute
import optitsp
from optimizetsp.solver import solve as joe


from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""
def plotGraph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_nodes(G, pos, node_color='c')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def sortedset(tas, loc): # gives TAs left in car, naive if ta walks home alone, let them
    d = {n:[] for n in G.neighbors(loc)}
    for t in tas:
        d[pcessors[t][loc]].append(t)
    pd = set()
    for key in d:
        if (len(d[key]) > 1):
            pd = pd.union(d[key])
    return [pd]



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

    class Car():
        def __init__(self, loc, tas, reached):
            self.loc = loc
            self.tas = tas # Make copies so don't run into any issues (probs don't have to do this bc I don't modify sets)
            self.reached = reached # Places I've been, but only once I've left

        def __eq__(self, other):
            return self.loc == other.loc and self.tas == other.tas # Don't need reached

        def __hash__(self):
            return (self.loc*self.loc << 32) + sum([l*l*l for l in self.tas])

        def __str__(self):
            return "Car({}, {}, {})".format(self.loc, self.tas, self.reached)

        def __repr__(self):
            return self.__str__()

        def neighbors(self):
            neighs = []
            if self.loc in self.reached: # If I've been here before, then can't drop anyone off
                for n in G.neighbors(self.loc):
                    cost = 2/3 * all_paths[self.loc][n]
                    car = Car(n, self.tas, self.reached)
                    neighs.append((car, cost))
            else:
                newreached = self.reached.union(set([self.loc]))
                # Trivial - drop everyone off and head home
                cost = 2/3 * all_paths[self.loc][starting_car_location] + sum([all_paths[self.loc][t] for t in self.tas])
                car = Car(starting_car_location, set(), newreached)
                neighs.append((car, cost))
                # Now try all ways of dropping people off
                tas = self.tas - {self.loc} # If I'm at a TA's home, drop them off
                pds = sortedset(tas, self.loc)
                pds_costs = [sum([all_paths[self.loc][t] for t in (tas - pd)]) for pd in pds]
                for pd, pdc in zip(pds, pds_costs):
                    for n in G.neighbors(self.loc):
                        cost = 2/3 * all_paths[self.loc][n] + pdc
                        car = Car(n, pd, newreached)
                        neighs.append((car, cost))
            return neighs


        def isDone(self):
            return self.loc == starting_car_location and len(self.tas) == 0

    # Create graph
    global G # Left here for debugging purposes
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)

    # Convert locations to indices
    list_of_homes = set([list_of_locations.index(h) for h in list_of_homes])
    starting_car_location = list_of_locations.index(starting_car_location)

    # Generate shortest path lengths to all nodes for dropoffs and returning to center
    global pcessors, all_paths
    pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)

    return semitree(list_of_locations, starting_car_location, list_of_homes, G)


def semitree(list_of_locations, starting_car_location, list_of_homes, G, subsolver = joe):
    if len(list_of_homes) == 0:
        return [starting_car_location], {}
    elif len(list_of_homes) == 1:
        return [starting_car_location], {starting_car_location: list_of_homes}
    _, all_paths = nx.floyd_warshall_predecessor_and_distance(G)
    #check if removing each vertex gives a disconnected graph, in DFS order
    bfs_iter = list(nx.bfs_successors(G, starting_car_location))

    #these guys are the ones we've checked through DFS, dont want to go backwards
    checked = set()

    bfs_vert = [bfs_iter[0][0]] + sum([[j for j in i[1]] for i in bfs_iter], []) #the nodes, in BFS order

    set_homes = set(list_of_homes)
    subs = {} #We're gonna store the subgraphs in G with keys the node removed to create that graph
    sub_homes = {} #dictionary of homes of subgraphs, with keys home.
    forced_visit = set() #if the subgraph contains 2 or more homes, then Rao must enter that subgraph. These are the subgraphs that have more than two homes
    for v in G.nodes:
        subs[v] = []
    for i in bfs_vert: #check removing nodes in BFS order
        checked.add(i) #these are the guys we checked
        G_copy = G.copy()
        if i in G_copy.nodes:
            G_copy.remove_node(i)
        temp = nx.connected_components(G_copy)
        connect = []

        for j in temp:
            temp_G = G.copy()
            for k in set(G.nodes) - j:
                temp_G.remove_node(k)
            temp_G.add_node(i)
            for edge in G.edges(i):
                if edge[0] in temp_G.nodes:
                    temp_G.add_edge(i, edge[1], weight = all_paths[i][edge[1]])
                elif edge[1] in temp_G.nodes:
                    temp_G.add_edge(i, edge[0], weight = all_paths[i][edge[0]])

            connect += [temp_G]

        if len(connect) > 1:
            for sub in connect:
                list_of_subhomes = []
                sup = True #is it maximal subgraph?
                subgraph_hash = 0




                for n in sub.nodes:
                    if n in checked:
                        sup = False #it contains points already checked, so not maximal (also don't want to consider the piece containing Soda Hall as a subgraph)
                        break
                    elif n in list_of_homes:
                        list_of_subhomes += [n]
                    subgraph_hash += n

                if sup:
                    sub_homes[subgraph_hash] = list_of_subhomes
                    if len(sub_homes[subgraph_hash]) > 0:
                        set_homes.add(i)
                    if len(sub_homes[subgraph_hash]) > 1:
                        forced_visit.add(i)

                    subs[i] += [sub]
                    for n in sub.nodes:
                        if n in G.nodes:
                            G.remove_node(n)


    list_of_homes = list(set_homes)
    forced_visit_list = list(forced_visit)
    source_homes = []
    for i in G.nodes:
        if i in list_of_homes:
            source_homes += [i]

    subsols = {} #solutions of subgraphs
    for v in subs:
        subsols[v] = []
    for v in subs:
        for s in subs[v]:
            plotGraph(s)
            s_hash = 0
            for n in s.nodes:
                s_hash += n
            a, b = semitree(v, sub_homes[s_hash], s)
            subsols[v] += [[a, b]]

    if len(source_homes) <= 5:
        dont_touch = set(forced_visit_list)
        listlocs, listdropoffs = brute.solve(starting_car_location, source_homes, G, dont_touch)
        return stitch(listlocs, listdropoffs, subsols)
    else:
    listlocs, listdropoffs = subsolver(source_homes, starting_car_location, G, solve_timeout = 10 forced_visit_indices = forced_visit_list)

    return stitch(listlocs, listdropoffs, subsols)









def stitch(listlocs, listdropoffs, subsols = {}): #"stitch together" the solutions of the subgraphs. subs a dictionary of subgraph solutions: keys are base vertices, paired with lists of lists of solutions of subgraphs for that base vertex
    for v in subsols:
        if v in listlocs:
            for s in subsols[v]:
                ind_v = listlocs.index(v)
                listlocs.remove(v)
                listlocs = listlocs[:ind_v] + s[0] + listlocs[ind_v:]
    for v in subsols:
        for sols in subsols[v]:
            listdropoffs = {**listdropoffs, **sols[1]}
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
