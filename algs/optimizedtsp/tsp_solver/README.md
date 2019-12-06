# TSP algorithm

*note that this is not a complete algorithm for the project

The idea is that we want to determine how accurate the solution returned by TSP is compared to the order that TAs are dropped off in the optimal solution. If we find that TSP is a good approximator of the order to drop off TAs, we can then try to optimize from a naive algorithm of dropping everyone at their homes using TSP.

We will use the library LocalSolver to approximate TSP (https://www.localsolver.com/download.html). We chose to use this library because they claim to be able to reach a 0.8% gap after a minute on the asymmetric TSPLib database.

In order to run the tsp_solver, you must install localsolver and obtain a free academic license.