import os
import sys
import subprocess
import argparse
from functools import reduce
sys.path.append("libs")
import utils
import optitsp
import brute
import gurobilp

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
    stas = set([list_of_locations.index(h) for h in list_of_homes])
    sloc = list_of_locations.index(starting_car_location)

    artmap = getArtmap(sloc, stas, G)

    listlocs, listdropoffs = treesolve(sloc, stas, G, artmap)

    t1 = time.perf_counter() - t0
    print(" done! Time: {}s".format(t1))

    return listlocs, listdropoffs

def getArtmap(sloc, stas, G):
    # Find biconnected components and get in nice form
    bccs = list(nx.biconnected_components(G))
    artpts = set(nx.articulation_points(G))

    # articulation point -> (biconnected component, entire subgraph involving bcc, artpts in that bcc)
    artmap = {i:[(b, set(), b.intersection(artpts) - {i}) for b in bccs if i in b] for i in artpts}
    if sloc not in artmap:
        cc = [i for i in bccs if sloc in i][0] # Find the biconnected component sloc is part of
        artmap[sloc] = [(cc, set(), cc.intersection(artpts))]

    # gets rid of parent in each set using BFS
    parents = {sloc}
    while parents:
        newparents = set()
        for p in parents:
            childs = set() # get all the children
            for t in artmap[p]:
                childs.update(t[2])
            for c in childs:
                artmap[c] = [i for i in artmap[c] if p not in i[0]] # remove the parent from all of them
                for t in artmap[c]:
                    t[2].difference_update({p})
            newparents.update(childs)
        parents = newparents

    generateSubgraphsDFS(artmap, sloc) # avoid too much recomputation and also pretty fun

    return artmap

def generateSubgraphsDFS(artmap, sloc):
    for bcc, subg, artps in artmap[sloc]:
        subg.update(bcc)
        for c in artps:
            generateSubgraphsDFS(artmap, c)
            for _, c_subg, _ in artmap[c]:
                subg.update(c_subg)

def treesolve(sloc, stas, G, artmap):
    lst_listlocs, lst_listdropoffs = [], []
    for bccset, subgset, artpts in artmap[sloc]:
        subg_tas = stas.intersection(subgset)
        if len(subg_tas) == 0:
            lst_listlocs.append([sloc])
            lst_listdropoffs.append({})
        elif len(subg_tas) == 1 or (len(subg_tas) == 2 and sloc in subg_tas):
            lst_listlocs.append([sloc])
            lst_listdropoffs.append({sloc:subg_tas})
        else:
            # Generate biconnected graph to run optitsp on
            bccg = G.subgraph(bccset).copy()
            bccorigtas = stas.intersection(bccset) # so we don't dropoff fake tas
            bcctas = bccorigtas.copy()
            bcctasmap = {} # for converting fake ta back to orig
            bccforceta = set()
            bccinsert = {} # Stores recursive calls to stitch in

            # Convert artpts to homes and perform recursive calls if necessary
            for ap in artpts:
                ap_subg = reduce(lambda a,b: a.union(b), [i[1] for i in artmap[ap]])
                ap_tas = stas.intersection(ap_subg)
                if len(ap_tas) == 1:
                    bcctas.add(ap)
                    bcctasmap[ap] = ap_tas.pop()
                elif len(ap_tas) >= 2: # if more than 2 tas then always optimal to enter subgraph
                    bcctas.add(ap)
                    bccforceta.add(ap)
                    bccinsert[ap] = treesolve(ap, ap_tas, G.subgraph(ap_subg).copy(), artmap)

            # Run optitsp (or brute)
            if len(bcctas) > 5:
                optitsp_locs, optitsp_dropoffs = optitsp.solve(sloc, bcctas, bccg, donttouch=bccforceta)
            else:
                optitsp_locs, optitsp_dropoffs = brute.solve(sloc, bcctas, bccg, donttouch=bccforceta)
            # Stitch everything together
            bcclocs = []
            bcc_inserted = []
            for i in optitsp_locs:
                if i in bccinsert and i not in bcc_inserted:
                    bcclocs.extend(bccinsert[i][0])
                    bcc_inserted.append(i) # don't double insert
                else:
                    bcclocs.append(i)
            bccdropoffs = {}
            for i in optitsp_dropoffs:
                newset = {bcctasmap[t] if t in bcctasmap else t for t in optitsp_dropoffs[i]}.intersection(stas)
                if len(newset) > 0: # possible for newset to be empty
                    bccdropoffs[i] = newset
            for i in bccinsert:
                for dppt in bccinsert[i][1]:
                    if dppt in bccdropoffs:
                        bccdropoffs[dppt].update(set(bccinsert[i][1][dppt]))
                    else:
                        bccdropoffs[dppt] = set(bccinsert[i][1][dppt])

            # Add to our running lists
            lst_listlocs.append(bcclocs)
            lst_listdropoffs.append(bccdropoffs)

    # Reconstruct listlocs and listdropoffs
    listlocs = lst_listlocs[0]
    listdropoffs = lst_listdropoffs[0]
    for l in lst_listlocs[1:]:
        listlocs.extend(l[1:])
    for dps in lst_listdropoffs[1:]:
        for d in dps:
            if d in listdropoffs:
                listdropoffs[d].update(dps[d])
            else:
                listdropoffs[d] = dps[d]

    # Convert all dropoff sets to lists
    for d in listdropoffs:
        listdropoffs[d] = list(listdropoffs[d])

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


        
