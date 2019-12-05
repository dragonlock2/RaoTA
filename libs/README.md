# libs

This folder serves as an archive for much of the scripts and folder organization used in the development of the brute force algorithm and brainstorming. It contains wrapper.py, which can be used to automate the entire workflow of input generation, input validation, solving, and output validation. It also compares algorithms against the naive solution.

Note: Due to how I wrote the scripts, only run scripts from the base directory and not this folder.

Here's some basic commands to run to check if everything is running properly:

```
python3 libs/wrapper.py -n 15 20 25 -e 1 -s algs/brutecppLVIII
python3 libs/wrapper.py -b
```

It also provides gurobilp.py, brute.py, optitsp.py, and minimp.py which are implementations of their corresponding algorithms available as subroutines.