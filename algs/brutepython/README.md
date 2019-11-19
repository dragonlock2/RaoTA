# Brute Force Python Algorithm

This algorithm uses a modified Dijkstra's algorithm to perform a brute force search for the optimal solution. It works decently for up to 30 locations and 15 TAs. This serves as a benchmark to measure against other algorithms.

Conceptually, it uses the concept of a Car object which has a location, TAs, and set of reached locations. The "neighboring vertices" of a Car are all possible ways to drop off its TAs at its current location and moving to a neighboring location. If a Car has reached its current location before, then it can't drop off there because it could've done so earlier. Also, if a Car drops off all its TAs, then it should return home immediately. The path reconstruction part of the algorithm handles the jump.