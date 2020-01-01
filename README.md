# RaoTA
CS 170 Fall 2019 Project

Matthew Tran, Kevin An, Joe Zou

[Problem Statement](docs/spec.pdf)

## How to Use

This section outlines the steps to run our code and generate outputs similar to what we have.

Note: As of 12/6/19, Gurobi, Google OR-Tools, and LocalSolver are only available on Python <=3.7 so we recommend using Python 3.7.

We had many headaches getting this to run on Linux and Windows, so we recommend MacOS.

Let's start by getting the numerous dependencies. Run everything from the base project folder unless otherwise noted.

### Installing Pip Libraries
```
pip3 install numpy
pip3 install networkx
pip3 install matplotlib
pip3 install heapdict
pip3 install ortools
```

### Compiling C++ Algorithms
```
sudo apt install libboost-all-dev # if on Linux
brew install boost # if on MacOS

cd algs/brutecppLVIII
make
cd ../brutecppCC
make
```
Note: If the code isn't compiling, try MacOS. We had some issues with Linux.

### Installing LocalSolver

LocalSolver offers a free academic license. A quick Google search should provide all the instructions for getting it up and running. Note that it does take about a day to acquire the free license.

### Installing Gurobi

Gurobi offers a free academic license. A quick Google search should provide all the instructions for getting it up and running. Basically make an account, download, and then set the key. Make sure to be on Airbears2 or eduroam when setting the key.

We didn't want to use Gurobi's version of Python, so we used their gurobipy module. Run the following from Gurobi's installation directory. On MacOS, we used Spotlight to help find it. If there's a setup.py in the folder you're in the right place.
```
python3 setup.py install
```

### Running Algorithms

Note to TAs: Copy over the inputs/ folder now and make an outputs/ folder.

We developed and ran several algorithms to get our outputs. Here's a tl;dr list of commands. We made a lot of little changes to our algorithms as we went along but we've done our best to ensure that running these commands will get outputs that are very close to what we have.

```
python3 sorter.py
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/trees outputs -t 3600
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/treeish outputs -t 3600
python3 bigsolve.py algs/brutecppCC orgin/bruteforceable/tspable outputs -t 3600
python3 bigsolve.py algs/optimizedtsp inputs outputs
python3 bigsolve.py algs/semitreeTSP inputs outputs
python3 bigsolve.py algs/minorimprove inputs outputs -t 3600
python3 bigsolve.py algs/semitreeILP inputs outputs -t 3600
```

Note that this can take quite awhile to finish. If you don't quite have the time, simply run the following and it should get outputs that are within about 2% of our best outputs (exactly our best in most cases) in about an hour.

```
python3 bigsolve.py algs/semitreeTSP inputs outputs
```

We generated all of our outputs using a 2018 Macbook Pro (i7-8850H), a 2016 Macbook Pro (i7-6820HQ), and a Hive machine (i7-4770).

And just like that you are done!

Check out [descripts.md](docs/descripts.md) for info about some scripts we wrote!

Check out [optimal.md](docs/optimal.md) for info on inputs we solved "optimally" and a bunch we didn't have the time to finish.