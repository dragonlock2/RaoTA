# RaoTA
CS 170 Fall 2019 Project

Matthew Tran, Kevin An, Joe Zou

[Problem Statement](spec.pdf)

## How to Use (Work in Progess)

This section outlines the steps to run our code and generate outputs similar to what we have, keeping in mind a degree of randomness present in parts of our algorithms.

Note: As of 12/1/19, Google OR-Tools and LocalSolver are only available on Python <=3.7 so we recommend sticking to Python 3.7.

### Dependencies
There's quite a few libraries to install.
```
pip3 install numpy
pip3 install networkx
pip3 install matplotlib
pip3 install heapdict
pip3 install ortools
# TODO localsolver install tutorial
```
The brute force algorithms are implemented in C++.
```
sudo apt install libboost-all-dev # if on Linux
brew install boost # if on MacOS
```
Now we need to compile the C++ algorithms.
```
cd algs/brutecppLVIII
make
cd ../brutecppCC
make
```
### Running Algorithms
We developed and ran several algorithms to get our outputs. Here's the tl;dr list of commands.

```
python3 sorter.py
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/trees outputs
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/treeish outputs
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/tspable outputs
# TODO how to run localsolver
python3 bigsolve.py algs/minorimprove inputs outputs
python3 bigsolve.py algs/experimental inputs outputs
```
It's possible to run the brute force parts faster using brutecppLVIII but this involves sorting out all 50.in bruteforceable inputs and running on those. The outputs are still the same so in the interest of time this is left as an exercise to the reader.

## Scripts

### bigsolve.py

This script is used to run a specified algorithm on a folder of inputs. It automatically moves outputs to the output folder if it is better than the existing output (or if there is no output existing). Try the following:

```
python3 sorter.py
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/trees outputs -t 20
```

The presence of a "Yeet!" indicates an output has been replaced.

### merge.py

This script is used to merge a given set of new outputs with the current set of outputs. Useful for when computation is done on separate computers and have to be merged. A good way to fix this is to move all new outputs into a temp/ folder and repulling the outputs. Then run the following:

```
python3 merge.py temp outputs
```

### sorter.py

This script sorts all the inputs/ based on certain criteria into orginout/. Mainly, it is used to sort inputs by size and completeness. It also maintains separate folders for bruteforceable inputs and inputs that don't maximize the given limits. This script can be run without arguments.

### benchmark.py

This script is used to record characteristics of optimal solutions for small input. It adds data on the number of nodes, multiplicative factor of extra edges, percent improvement over naive, and percent of total cost that is driving to a csv file which can be analyzed later. Try the following command:

```
python3 benchmark.py -f test.csv 3 15 0 15 1
```

We denote a measure of "tree-ness" as the multplicative factor divided by the total number of nodes. That is, 0 represents being a tree and 1 represents being complete. One thing that's interesting about our data is that as the graph becomes more complete, the percent improvement over the naive gets upper bounded at 30%. Also interesting to note is that the optimal becomes all driving (TSP) when the "tree-ness" factor is above around 0.2.

### graphvis.py

This script is used to view a .in file or all the .in files in a folder. To run it do:

```
python3 graphvis.py inputs
```

To move onto the next graph, just click or press a key while in the matplotlib image. To stop early, go to your terminal and issue a KeyboardInterrupt. Then close the matplotlib plot.

### checkout.py

This script prints out all files that we don't have a solution to yet. Run without arguments.