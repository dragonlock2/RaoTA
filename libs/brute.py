import networkx as nx
import heapdict as hd
from itertools import chain, combinations

def powerset(iterable): # NOTE: this doesn't include empty
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))

def solve(sloc, stas, G, pcessors, all_paths):
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
                cost = 2/3 * all_paths[self.loc][sloc] + sum([all_paths[self.loc][t] for t in self.tas])
                car = Car(sloc, set(), newreached)
                neighs.append((car, cost))
                # Now try all ways of dropping people off
                tas = self.tas - {self.loc} # If I'm at a TA's home, drop them off
                pds = [set(pd) for pd in powerset(tas)]
                pds_costs = [sum([all_paths[self.loc][t] for t in (tas - pd)]) for pd in pds]
                for pd, pdc in zip(pds, pds_costs):
                    for n in G.neighbors(self.loc):
                        cost = 2/3 * all_paths[self.loc][n] + pdc
                        car = Car(n, pd, newreached)
                        neighs.append((car, cost))
            return neighs


        def isDone(self):
            return self.loc == sloc and len(self.tas) == 0

    # Initialize variables for Dijkstra's
    pq = hd.heapdict()
    startcar = Car(sloc, stas.copy(), set())
    paths, costs = {}, {}

    # Add source point
    pq[startcar] = 0
    paths[startcar] = None
    costs[startcar] = 0

    inf = float('inf')

    # Run Dijkstra's
    while pq:
        # Pop off smallest in PQ
        car, currcost = pq.popitem()

        if car.isDone():
            break

        for ncar, ncost in car.neighbors():
            # Relax all edges
            ncost += currcost
            if ncost < costs.setdefault(ncar, inf):
                pq[ncar] = ncost
                costs[ncar] = ncost
                paths[ncar] = car

    # Reconstruct min path
    minpath = []
    currcar = Car(sloc, set(), set())
    while currcar != startcar:
        currcar = paths[currcar]
        minpath.append(currcar)
    minpath = minpath[::-1]
    # Didn't append end node yet so we can append shortest paths to it
    pathback = nx.reconstruct_path(minpath[-1].loc, sloc, pcessors)[1:-1] # Don't include first or last because already there
    for n in pathback:
        minpath.append(Car(n, set(), set()))
    minpath.append(Car(sloc, set(), set()))

    # Convert to format for saving
    listlocs, listdropoffs = [], {}
    for i in range(len(minpath)):
        listlocs.append(minpath[i].loc)
        if (i < len(minpath) - 1):
            drops = minpath[i].tas - minpath[i+1].tas
            if len(drops) > 0:
                listdropoffs[minpath[i].loc] = list(drops)

    # Naive case
    if len(listlocs) == 2:
        listlocs = listlocs[:1]

    return listlocs, listdropoffs