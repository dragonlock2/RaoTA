# RaoTA
CS 170 Fall 2019 Project

Matthew Tran, Kevin An, Joe Zou

[Problem Statement](spec.pdf)

## How To Use

First install some python libraries.

```
pip3 install numpy
pip3 install networkx
pip3 install matplotlib
```

If using C++ algs, might want to install boost libraries.

```
sudo apt install libboost-all-dev # if on Linux
brew install boost # if on MacOS
```

The main script to run is wrapper.py. It performs the entire workflow of generating inputs, validating them, solving them with the chosen algorithm, solving them naively, and finally validating the outputs and displaying results. Optionally, it also archives the input and output files. Run the below command for a basic test.

```
python3 wrapper.py -n 5 10 15
```

For generating inputs, use inputgen.py. To ensure triangle inequality is satisfied, it does this by plotting locations as a bunch of points on a 2D graph and using distances between points to determine edge weights. To ensure connectivity, it first constructs a random tree of all points. Then it adds a bunch of edges to increase complexity. Run below to generate an example input.

```
python3 inputgen.py inputs/15.in 15 10 10
```

To learn more about all parameters in each script just run:

```
python3 <script name>.py -h
```

## Algorithms

All algorithms are stored in the algs folder. To run an algorithm, specify the folder in wrapper.py. For example, to run sortedpython, run:

```
python3 wrapper.py -s algs/sortedpython
```