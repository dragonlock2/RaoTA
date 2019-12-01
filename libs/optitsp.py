import networkx as nx

# Run in python3.7 (for now)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Provides a subroutine to run optimizedtsp

def solve(sloc, stas, G, pcessors, alldists, donttouch=[], timeout=2):
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
    # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH) # Uncomment if want even better cycle
    # search_parameters.time_limit.seconds = timeout
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

    # Optimize TSP solution
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

    # Reconstruct dropoffs
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

    # Reconstruct full cycle
    listlocs = []
    curr = -1
    for i in range(len(drop_cycle)-1):
        curr = drop_cycle[i]
        while curr != drop_cycle[i+1]:
            listlocs.append(curr)
            curr = pcessors[drop_cycle[i+1]][curr]
    listlocs.append(curr)

    return listlocs, listdropoffs

    





