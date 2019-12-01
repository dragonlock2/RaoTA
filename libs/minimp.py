import networkx as nx
import brute

# Run in python3.7 (for now)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Implementation of minorimprove available as a subroutine
# First makes sure no edges are double traveled by TAs and then runs TSP to optimize dropoff cycle

def improve(sloc, stas, G, listlocs, listdropoffs):
    pcessors, alldists = nx.floyd_warshall_predecessor_and_distance(G)

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
                lilo, lidr = brute.solve(c[0], set(g), G) # brute force to determine optimal dropoff of rest of guys
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
    if sloc not in listdps:
        listdps.append(sloc)

    dpmap = {i:listdps[i] for i in range(len(listdps))}
    data_dist = [[0 for _ in range(len(dpmap))] for _ in range(len(dpmap))]
    for i in range(len(data_dist)):
        for j in range(len(data_dist)):
            data_dist[i][j] = int(alldists[dpmap[i]][dpmap[j]]*1000000) # OR tools only uses integers
    data_num_vehicles = 1
    data_depot = -1 # starting location
    for key in dpmap:
        if dpmap[key] == sloc:
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
    # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    # search_parameters.time_limit.seconds = 5
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

    return listlocs, listdropoffs
