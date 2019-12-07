# Semitree TSP Implementation

Alternative implementation of semitreepython.

Conceptually, it identifies tree-like structures in graphs and applies our theorems to solve them more optimally. For parts that aren't tree-like, which is basically all biconnected components, it runs optitsp. If the part if sufficiently small, it runs brute. This algorithm strives to address the weakness of the shotgun-like approach optitsp takes to optimize from the TSP solution.

While not optimal, this algorithm is exceptionally fast, completing all inputs with an average of ~2.5s and within ~2% of our best outputs if not the best in most cases.