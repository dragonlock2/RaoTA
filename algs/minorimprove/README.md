# Minor Improvement Alg

Note: Only run this when a solution for all inputs has been found. It may also take a few runs until no improvements can be easily made.

Note2: Google OR-Tools as of 11-29-19 only supports up to Python 3.7 so modify scripts accordingly.

This algorithm takes in a solution and identifies parts that can be easily improved and does them. It identifies groups of TAs that follow the same edge home and runs brute force to figure out a more optimal dropoff ordering.

It also performs TSP (Google OR-Tools) afterward on the remaining dropoff points to optimize further.