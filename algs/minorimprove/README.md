# Minor Improvement Alg

Note: Only run this when a solution for all inputs has been found. It may also take a few runs until no improvements can be easily made.

Note2: Google OR-Tools and Gurobi as of 12-6-19 only support up to Python 3.7 so use that.

This algorithm takes in a solution and identifies parts that can be easily improved and does them. It identifies groups of TAs that follow the same edge home and runs brute force to figure out a more optimal dropoff ordering. Afterwards, it performs TSP (Gurobi ILP) on the remaining dropoff points to optimize further.