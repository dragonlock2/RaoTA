import os
import sys
import subprocess
sys.path.append("libs")
import argparse
import utils

from student_utils import *

from gurobipy import *
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
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    t0 = time.perf_counter()

    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    nnodes = len(list_of_locations)
    stas = {list_of_locations.index(h) for h in list_of_homes}
    sloc = list_of_locations.index(starting_car_location)
    pcessors, alldists = nx.floyd_warshall_predecessor_and_distance(G)

    m = Model()

    """ Add variables and objective """

    # Decision variable for each edge, if pick it, adds driving cost, directed to simplify things
    e = {}
    for i in range(nnodes):
        for j in range(nnodes):
            e[i,j] = m.addVar(obj=2/3*alldists[i][j], vtype=GRB.BINARY, name="e{}_{}".format(i, j))
    m.update()

    # Decision variable for each TA at each vertex, if pick it, TA walks home from there
    v = {}
    for i in range(nnodes):
        for k in stas:
            v[i,k] = m.addVar(obj=alldists[i][k], vtype=GRB.BINARY, name="v{}_{}".format(i, k))
    m.update()

    # Indicator variables, if 1 then this is a dropoff point, 0 otherwise
    ind = {}
    for i in range(nnodes):
        ind[i] = m.addVar(vtype=GRB.BINARY, name="ind"+str(i))
    m.update()

    # Sum variable to count number of non-home dropoffs
    sumtot = m.addVar(name="sumtot")
    m.update()

    # Indicator variable if there is a non-home dropoffs
    indtot = m.addVar(vtype=GRB.BINARY, name="indtot")
    m.update()

    """ Add constraints """

    # No self loops
    for i in range(nnodes):
        e[i,i].ub = 0
    m.update()

    # All TAs must be dropped off and only once
    for k in stas:
        m.addLConstr(quicksum(v[i,k] for i in range(nnodes)) == 1)
    m.update()

    # Setup dropoff indicators
    for i in range(nnodes):
        m.addGenConstrOr(ind[i], [v[i,k] for k in stas])
    m.update()

    # Add non-home sum constraint
    m.addLConstr(quicksum(ind[i] for i in range(nnodes) if i != sloc) == sumtot)
    m.update()

    # Setup non-home indicator
    m.addGenConstrOr(indtot, [ind[i] for i in range(nnodes) if i != sloc])
    m.update()

    # Add in and out degree constraints for non-home vertices
    for i in range(nnodes):
        if i != sloc:
            m.addLConstr(quicksum(e[i,j] for j in range(nnodes)) == ind[i])
            m.addLConstr(quicksum(e[j,i] for j in range(nnodes)) == ind[i])
    m.update()

    # Add constraints for home, if non-home dropoff, then must leave and come back
    m.addGenConstrIndicator(indtot, True, quicksum(e[sloc,i] for i in range(nnodes)) == 1.0)
    m.addGenConstrIndicator(indtot, True, quicksum(e[i,sloc] for i in range(nnodes)) == 1.0)

    # Limit number of edges to form a cycle through dropoffs
    expr = 0
    for i in range(nnodes):
        for j in range(nnodes):
            expr += e[i,j]
    m.addGenConstrIndicator(indtot, True, expr == sumtot + 1)

    """ Add callback to handle subtours """

    def cbSubtourElim(model, where):
        if where == GRB.callback.MIPSOL:
            ed = [] # make list of selected edges
            for i in range(nnodes):
                sol = model.cbGetSolution([e[i,j] for j in range(nnodes)]);
                ed += [(i,j) for j in range(nnodes) if sol[j] > 0.5]
            cycles = getCycles(ed)
            if len(cycles) > 1: # if more than 1 cycle, then we have a subtour
                for c in cycles:
                    expr = 0 # all edges in the subgraph must total < |S|-1
                    for i in c:
                        for j in c:
                            expr += e[i,j]
                    model.cbLazy(expr <= len(c) - 1)        

    def getCycles(edges):
        visited = {i[0]:False for i in edges}
        nexts = {i[0]:i[1] for i in edges}
        cycles = []

        while True:
            curr = -1
            for i in visited:
                if visited[i] == False:
                    curr = i
                    break
            if curr == -1:
                break
            thiscycle = []
            while not visited[curr]:
                visited[curr] = True
                thiscycle.append(curr)
                curr = nexts[curr]
            cycles.append(thiscycle)

        return cycles

    """ Run optimizer """

    m.params.LazyConstraints = 1
    m.optimize(cbSubtourElim)

    """ Reconstruct solution """

    # Get travel cycle
    ed = [] # get selected edges
    edec = m.getAttr('x', e)
    for i in range(nnodes):
        for j in range(nnodes):
            if edec[i,j] > 0.5:
                ed.append((i,j))
    cycles = getCycles(ed) # find the one cycle
    if cycles:
        c = cycles[0] # rearrange so sloc first
        indstart = c.index(sloc)
        jumpcycle = c[indstart:] + c[:indstart] + [sloc]
    else:
        jumpcycle = [sloc]

    # Reconstruct intermediate nodes
    listlocs = []
    curr = -1
    for i in range(len(jumpcycle)-1):
        curr = jumpcycle[i]
        while curr != jumpcycle[i+1]:
            listlocs.append(curr)
            curr = pcessors[jumpcycle[i+1]][curr]
    listlocs.append(curr)

    # Get list of dropoffs
    vdec = m.getAttr('x', v)
    listdropoffs = {}
    for i in range(nnodes):
        for k in stas:
            if vdec[i,k] > 0.5:
                if i in listdropoffs:
                    listdropoffs[i].append(k)
                else:
                    listdropoffs[i] = [k]

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
