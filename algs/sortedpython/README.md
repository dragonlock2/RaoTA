# Sorted Python

This algorithm is very similar to brutepython but should reduce the runtime to roughly polynomial time. Instead of considering all possible subsets of the TAs in a Car, we instead first sort the TAs by distance from their homes. Now we pick sublists of increasing size, starting with no elements, then the 1st element, then the 1st and 2nd, and so on. Note that these sublists represent the TAs left in the car after the dropoff.

Note that there is a constant factor specifying the fraction of TAs that can remain in the car. Empirically, if it is set to 1, then random size 30 inputs are solved to within ~10% of the optimal. Above size 50, the factor must be set to <1 to solve in reasonable time. Around 0.7 works well for size 100 and 200 inputs. However, in those cases there is around only a 5% to 40% improvement over the naive solution. Generally speaking for small inputs the optimal is around a 50% to 75% improvement over the naive.

Note: sortedpython is guaranteed to perform at least as well as the naive solution.