# Experimental Algorithm

Place to try out new things. Currently setup as an alternate implementation of semitreepython. Performs very well, but can make even better if improve optitsp.

Conceptually, it identifies tree-like structures in graphs and applies our theorems to solve them more optimally. For parts that aren't tree-like, which is basically all biconnected components, it runs optitsp. If the part if sufficiently small, it runs brute. This algorithm strives to address the weakness of the shotgun-like approach optitsp takes to optimize from the TSP solution.