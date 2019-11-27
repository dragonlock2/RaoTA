# RaoTA
CS 170 Fall 2019 Project

Matthew Tran, Kevin An, Joe Zou

[Problem Statement](spec.pdf)

## How to Use
TODO

## Scripts

### bigsolve.py

TODO

### analyze.py

TODO

### benchmark.py

This script is used to record characteristics of optimal solutions for small input. It adds data on the number of nodes, multiplicative factor of extra edges, percent improvement over naive, and percent of total cost that is driving to a csv file which can be analyzed later. Try the following command:

```
python3 benchmark.py -f test.csv 3 15 0 15 1
```

We denote a measure of "tree-ness" as the multplicative factor divided by the total number of nodes. That is, 0 represents being a tree and 1 represents being complete. One thing that's interesting about our data is that as the graph becomes more complete, the percent improvement over the naive gets upper bounded at 30%. Also interesting to note is that the optimal becomes all driving (TSP) when the "tree-ness" factor is above around 0.2.

### graphvis.py

This script is used to view all the .in files in a folder. To run it do:

```
python3 graphvis.py inputs
```

To move onto the next graph, just click or press a key while in the matplotlib image. To stop early, go to your terminal and issue a KeyboardInterrupt. Then close the matplotlib plot.

### sorter.py

This script sorts all the inputs/ based on certain criteria into orginout/. Mainly, it is used to sort inputs by size and completeness. It also maintains separate folders for bruteforceable inputs and inputs that don't maximize the given limits. This script can be run without arguments.