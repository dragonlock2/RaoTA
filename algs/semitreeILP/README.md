# Semitree ILP Implementation

Alternative implementation of semitreepython. See semitreeTSP for a rough explanation of how this algorithm works. It uses gurobilp as a subsolver instead of optitsp.

This algorithm uses an ILP algorithm to "optimally" solve subgraphs that we find. As a result, this algorithm can take just about forever on a couple of specific inputs. However, it should find "provably optimal" solutions according to Gurobi on inputs that it does complete on.