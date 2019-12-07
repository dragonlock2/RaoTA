import networkx as nx

from gurobipy import *

# Provides a subroutine to run gurobilp

def solve(sloc, stas, G, donttouch=set()):
    pcessors, alldists = nx.floyd_warshall_predecessor_and_distance(G)

    nodes = set(G.nodes)

    m = Model()

    """ Add variables and objective """

    # Decision variable for each edge, if pick it, adds driving cost, directed to simplify things
    e = {}
    for i in nodes:
        for j in nodes:
            e[i,j] = m.addVar(obj=2/3*alldists[i][j], vtype=GRB.BINARY, name="e{}_{}".format(i, j))
    m.update()

    # Decision variable for each TA at each vertex, if pick it, TA walks home from there
    v = {}
    for i in nodes:
        for k in stas:
            v[i,k] = m.addVar(obj=alldists[i][k], vtype=GRB.BINARY, name="v{}_{}".format(i, k))
    m.update()

    # Indicator variables, if 1 then this is a dropoff point, 0 otherwise
    ind = {}
    for i in nodes:
        ind[i] = m.addVar(vtype=GRB.BINARY, name="ind"+str(i))
    m.update()

    # # Sum variable to count number of non-home dropoffs
    # sumtot = m.addVar(name="sumtot")
    # m.update()

    # # Indicator variable if there is a non-home dropoffs
    # indtot = m.addVar(vtype=GRB.BINARY, name="indtot")
    # m.update()

    """ Add constraints """

    # Force dropoffs
    for i in donttouch:
        m.addLConstr(v[i,i] == 1)
    m.update()

    # No self loops
    for i in nodes:
        e[i,i].ub = 0
    m.update()

    # All TAs must be dropped off and only once
    for k in stas:
        m.addLConstr(quicksum(v[i,k] for i in nodes) == 1)
    m.update()

    # Setup dropoff indicators
    for i in nodes:
        m.addGenConstrOr(ind[i], [v[i,k] for k in stas])
    m.update()

    # # Add non-home sum constraint
    # m.addLConstr(quicksum(ind[i] for i in nodes if i != sloc) == sumtot)
    # m.update()

    # # Setup non-home indicator
    # m.addGenConstrOr(indtot, [ind[i] for i in nodes if i != sloc])
    # m.update()

    # Add in and out degree constraints for non-home vertices
    for i in nodes:
        if i != sloc:
            m.addLConstr(quicksum(e[i,j] for j in nodes) == ind[i])
            m.addLConstr(quicksum(e[j,i] for j in nodes) == ind[i])
    m.update()

    # # Add constraints for home, if non-home dropoff, then must leave and come back
    # m.addGenConstrIndicator(indtot, True, quicksum(e[sloc,i] for i in nodes) == 1.0)
    # m.addGenConstrIndicator(indtot, True, quicksum(e[i,sloc] for i in nodes) == 1.0)

    # Add constraints for home, if non-home dropoff, then must leave and come back
    m.addLConstr(quicksum(e[sloc,i] for i in nodes) == 1.0)
    m.addLConstr(quicksum(e[i,sloc] for i in nodes) == 1.0)

    # # Limit number of edges to form a cycle through dropoffs
    # expr = 0
    # for i in nodes:
    #     for j in nodes:
    #         expr += e[i,j]
    # m.addGenConstrIndicator(indtot, True, expr == sumtot + 1)

    """ Add callback to handle subtours """

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

    """ Run optimizer """

    m.params.TimeLimit = 1200 # allow only 20 min
    # m.params.MIPGap = 0.05 # allow 5% tolerance
    m.params.MIPFocus = 2 # focus on optimality
    m.params.LazyConstraints = 1
    m.optimize(cbSubtourElim)

    """ Reconstruct solution """

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
        jumpcycle = [sloc, sloc]

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
    for i in nodes:
        for k in stas:
            if vdec[i,k] > 0.5:
                if i in listdropoffs:
                    listdropoffs[i].append(k)
                else:
                    listdropoffs[i] = [k]

    return listlocs, listdropoffs