# libs

This folder serves as an archive for much of the scripts and folder organization used in the development of the brute force algorithm and brainstorming. It contains wrapper.py, which can be used to automate the entire workflow of input generation, input validation, solving, and output validation. It also compares algorithms against the naive solution.

Note: Due to how I wrote the scripts, only run scripts from the base directory and not this folder.

Here's some basic commands to run to check if everything is running properly:

```
python3 libs/wrapper.py -n 15 20 25 -e 1 -s algs/brutecppLVIII
python3 libs/wrapper.py -b
```

It also provides gurobilp.py, brute.py, optitsp.py, and minimp.py which are implementations of their corresponding algorithms available as subroutines.

## Available subsolvers
This is also the home to a couple of our algorithms implemented as a subroutine. Unlike their main algorithm counterparts, they also take in a forced dropoff parameter.
### gurobilp.py
ILP reduction of the problem. In order to vastly improve runtime, it does not work on inputs where the naive solution is optimal.
### brute.py
Brute force algorithm. Like brutepython but kind of not really. Really only works well on less than 8 TAs.
### optitsp.py
Optimized TSP but uses Google OR-Tools and Gurobi instead of LocalSolver. Also includes a bit of minorimprove reoptimizes the dropoff cycle afterwards. It's currently setup to use Gurobi but we have kept the Google OR-Tools implementation for legacy support.
### minimp.py
Minor improvement algorithm using Google OR-Tools. Doesn't support forced dropoffs. Not recommended for use in new algorithms.