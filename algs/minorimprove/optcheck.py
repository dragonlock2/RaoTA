import sys, glob, subprocess, argparse, os, shutil, time
import networkx as nx
sys.path.append("libs/")
import output_validator as ov
import student_utils as su
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Performs basic checks to see if can improve an output.")
    parser.add_argument("inputs", type=str, help="Folder with *.in files")
    parser.add_argument("outputs", type=str, help="Folder with *.out files")
    args = parser.parse_args()

    for infile in sorted(glob.glob(args.inputs + "/*.in")):
        outfile = args.outputs + "/" + os.path.splitext(os.path.basename(infile))[0] + ".out"

        if not os.path.exists(outfile):
            continue

        print("Processing {}...".format(infile))

        input_data = utils.read_file(infile)
        num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = su.data_parser(input_data)
        G, _ = su.adjacency_matrix_to_graph(adjacency_matrix)

        list_of_homes = [list_locations.index(h) for h in list_houses]
        starting_car_location = list_locations.index(starting_car_location)

        f = open(outfile)
        listlocs = f.readline().strip().split(" ")
        listlocs = [list_locations.index(h) for h in listlocs]
        listdropoffs = []
        for i in range(int(f.readline())):
            listdropoffs.append([list_locations.index(h) for h in f.readline().strip().split(" ")])
        dropcycle = [(i, []) for i in listlocs]
        for i in listdropoffs:
            dropcycle[listlocs.index(i[0])][1].extend(i[1:])
        f.close()

        pcessors, all_paths = nx.floyd_warshall_predecessor_and_distance(G)

        for c in dropcycle:
            d = {n:[] for n in G.neighbors(c[0])}
            for t in c[1]:
                if t != c[0]:
                    d[pcessors[t][c[0]]].append(t)
            for key in d:
                if len(d[key]) > 1:
                    print("\t{} share a path at {}!".format(d[key], c[0]))

