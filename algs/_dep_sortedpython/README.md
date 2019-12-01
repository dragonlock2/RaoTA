# Deprecated - Sorted Python

This algorithm is very similar to brutepython but should reduce the runtime to roughly polynomial time. Instead of considering all possible subsets of the TAs in a Car, we instead first sort the TAs by distance from their homes. Now we pick sublists of increasing size, starting with no elements, then the 1st element, then the 1st and 2nd, and so on. Note that these sublists represent the TAs left in the car after the dropoff. Also to reduce a bit of memory usage, we only consider Cars when they're are at least as good as the naive solution.

Note that there are two constant factors specifying how many TAs must be dropped off at each location and the minimum kept in the car. With values of 0.55 to 0.6, it performs about 18% better than the naive. As graphs become more complete, performance drops off to naive solution. We conjecture this is because TSP becomes optimal as connectedness increases.

Note: sortedpython is guaranteed to perform at least as well as the naive solution.

Deprecated because in favor of our newer algorithms. This one is too slow and provides subpar solutions.