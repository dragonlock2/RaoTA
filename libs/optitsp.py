import networkx as nx

# Run in python3.7 (for now)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from gurobipy import *

# Provides a subroutine to run optimizedtsp

def solve(sloc, stas, G, donttouch=set()):
    pcessors, alldists = nx.floyd_warshall_predecessor_and_distance(G)

    ta_cycle = gurobiTspCycle(sloc, stas, alldists)
    drop_cycle = optCycle(ta_cycle, alldists, donttouch)
    listdropoffs = reconDropoffs(sloc, stas, ta_cycle, drop_cycle)
    if (len(listdropoffs) > 1):
        drop_cycle = gurobiTspCycle(sloc, set(listdropoffs.keys()), alldists)
    listlocs = reconLocs(drop_cycle, pcessors)

    return listlocs, listdropoffs

# Finds TSP cycle starting at sloc and goes through all stas
# Does not reconstruct full cycle, just finds how to reach each TA
# If timeout specified, will search for that long
def tspCycle(sloc, stas, alldists, timeout=0):
    # Generate data for TSP
    dp_list = list(stas) # list of all nodes that must be visited
    if sloc not in dp_list:
        dp_list.append(sloc)
    dp_map = {i:dp_list[i] for i in range(len(dp_list))} # map to 0,1,2,... for use with OR-tools
    dp_dist = [[0 for _ in range(len(dp_map))] for _ in range(len(dp_map))] # for distances between nodes
    for i in range(len(dp_dist)):
        for j in range(len(dp_dist)):
            dp_dist[i][j] = int(alldists[dp_map[i]][dp_map[j]]*1000000) # OR tools only uses integers
    dp_num_vehicles = 1 # only got one car to drive TAs home
    dp_depot = -1 # starting location
    for key in dp_map:
        if dp_map[key] == sloc:
            dp_depot = key
            break

    # Run TSP
    manager = pywrapcp.RoutingIndexManager(len(dp_dist), dp_num_vehicles, dp_depot)
    routing = pywrapcp.RoutingModel(manager)
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dp_dist[from_node][to_node]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    if timeout:
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = timeout
    assignment = routing.SolveWithParameters(search_parameters)
    if not assignment:
        raise Exception("Nani TSP didn't work!")
    # Reconstruct cycle, gives ordering to drop off TAs
    ta_cycle = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        ta_cycle.append(manager.IndexToNode(index))
        index = assignment.Value(routing.NextVar(index))
    ta_cycle.append(manager.IndexToNode(index))
    ta_cycle = [dp_map[i] for i in ta_cycle]

    return ta_cycle

def gurobiTspCycle(sloc, stas, alldists):
    m = Model()

    nodes = set(stas).union({sloc})

    # Add variable for each edge
    e = {}
    for i in nodes:
        for j in nodes:
            e[i,j] = m.addVar(obj=alldists[i][j], vtype=GRB.BINARY, name="e{}_{}".format(i, j))
    m.update()

    # Add degree 2 constraint for all vertices
    for i in nodes:
        m.addConstr(quicksum(e[i,j] for j in nodes) == 1)
        m.addConstr(quicksum(e[j,i] for j in nodes) == 1)
        e[i,i].ub = 0
    m.update()

    # Add lazy constraint
    def cbSubtourElim(model, where):
        if where == GRB.callback.MIPSOL:
            ed = [] # make list of selected edges
            for i in nodes:
                for j in nodes:
                    sol = model.cbGetSolution(e[i,j]);
                    if sol > 0.5:
                        ed += [(i,j)]
            cycles = getCycles(ed)
            if len(cycles) > 1: # if more than 1 cycle, then we have a subtour
                for c in cycles:
                    expr = 0 # all edges in the subgraph must total <= |S|-1
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

    m.params.LazyConstraints = 1
    m.optimize(cbSubtourElim)

    # Get travel cycle
    ed = [] # get selected edges
    edec = m.getAttr('x', e)
    for i in nodes:
        for j in nodes:
            if edec[i,j] > 0.5:
                ed.append((i,j))
    cycles = getCycles(ed) # find the one cycle
    if cycles:
        c = cycles[0] # rearrange so sloc first
        indstart = c.index(sloc)
        jumpcycle = c[indstart:] + c[:indstart] + [sloc]
    else:
        jumpcycle = [sloc]

    return jumpcycle

# Runs basic optimization on TSP cycle, just tries alternate dropoff points
def optCycle(ta_cycle, alldists, donttouch):
    drop_cycle = ta_cycle.copy() # Find best location to dropoff corresponding TA in ta_cycle, initially just the TA's home
    for _ in range(len(drop_cycle)): # Doing this enough times hopefully does a good job
        for i in range(1, len(drop_cycle) - 1): # Check for better dropoff location for each TA
            if ta_cycle[i] not in donttouch:
                min_j, min_cost = -1, float('inf')
                for j in alldists[ta_cycle[i]]: # Check all other possible dropoff points, literally all nodes
                    ncost = 2/3*alldists[j][drop_cycle[i-1]] + alldists[j][ta_cycle[i]] + 2/3*alldists[j][drop_cycle[i+1]] 
                    # Cost to drive to new node (from previous in cycle), dropoff, and drive to next node
                    if ncost < min_cost:
                        min_j, min_cost = j, ncost
                drop_cycle[i] = min_j
    return drop_cycle

# Reconstructs dropoffs
def reconDropoffs(sloc, stas, ta_cycle, drop_cycle):
    listdropoffs = {}
    for i in range(1, len(ta_cycle)-1):
        if drop_cycle[i] in listdropoffs:
            listdropoffs[drop_cycle[i]].append(ta_cycle[i])
        else:
            listdropoffs[drop_cycle[i]] = [ta_cycle[i]]
    # Edge case: TA home = starting location
    if sloc in stas:
        if sloc in listdropoffs:
            listdropoffs[sloc].append(sloc)
        else:
            listdropoffs[sloc] = [sloc]
    return listdropoffs

# Reconstructs dropoff cycle
def reconLocs(drop_cycle, pcessors):
    listlocs = []
    curr = -1
    for i in range(len(drop_cycle)-1):
        curr = drop_cycle[i]
        while curr != drop_cycle[i+1]:
            listlocs.append(curr)
            curr = pcessors[drop_cycle[i+1]][curr]
    listlocs.append(curr)
    return listlocs