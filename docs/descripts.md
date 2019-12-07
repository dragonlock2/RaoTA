# Descriptions of a Couple of Scripts

## bigsolve.py

This script is used to run a specified algorithm on a folder of inputs. It automatically moves outputs to the output folder if it is better than the existing output (or if there is no output existing). Try the following:

```
python3 sorter.py
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/trees outputs -t 20
```

The presence of a "Yeet!" indicates an output has been replaced.

## merge.py

This script is used to merge a given set of new outputs with the current set of outputs. Useful for when computation is done on separate computers and have to be merged. A good way to fix this is to move all new outputs into a temp/ folder and repulling the outputs. Then run the following:

```
python3 merge.py temp outputs
```

## sorter.py

This script sorts all the inputs/ based on certain criteria into orginout/. Mainly, it is used to sort inputs by size and completeness. It also maintains separate folders for bruteforceable inputs and inputs that don't maximize the given limits. This script can be run without arguments.

## copyin.py

Copies files entered into a popup Sublime text file from input folder to output folder. Useful for copying over our files that took too long. Try the following:

```
python3 copyin.py -i orgin -o tmplong
```

## removin.py

Removes files entered into a popup Sublime text file from input folder. Useful for removing files that we already know the solution to or that simply take too long. Try the following:

```
python3 removin.py tmplong
```

## benchmark.py

This script is used to record characteristics of optimal solutions for small input. It adds data on the number of nodes, multiplicative factor of extra edges, percent improvement over naive, and percent of total cost that is driving to a csv file which can be analyzed later. Try the following command:

```
python3 benchmark.py -f test.csv 3 15 0 15 1
```

We denote a measure of "tree-ness" as the multplicative factor divided by the total number of nodes. That is, 0 represents being a tree and 1 represents being complete. One thing that's interesting about our data is that as the graph becomes more complete, the percent improvement over the naive gets upper bounded at 30%. Also interesting to note is that the optimal becomes all driving (TSP) when the "tree-ness" factor is above around 0.2.

After running our solvers on all inputs, we realize our findings pretty much only apply to random graphs.

## graphvis.py

This script is used to view a .in file or all the .in files in a folder. To run it do:

```
python3 graphvis.py inputs
```

To move onto the next graph, just click or press a key while in the matplotlib image. To stop early, go to your terminal and issue a KeyboardInterrupt. Then close the matplotlib plot.