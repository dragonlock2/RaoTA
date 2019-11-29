import sys, glob, subprocess, argparse, os
import networkx as nx
import matplotlib.pyplot as plt
sys.path.append("libs/")
import student_utils as su
import utils

def displayFile(input_file):
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = su.data_parser(input_data)
    G, _ = su.adjacency_matrix_to_graph(adjacency_matrix)

    list_of_homes = set([list_locations.index(h) for h in list_houses])
    starting_car_location = list_locations.index(starting_car_location)

    plt.figure(3,figsize=(14,8))
    pos = nx.spring_layout(G)
    cmap = []
    for node in G:
        if node == starting_car_location:
            cmap.append('r')
        elif node in list_of_homes:
            cmap.append('g')
        else:
            cmap.append('c')
    nx.draw_networkx_nodes(G, pos, node_color=cmap)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close()


def plotGraph():
    pos = {i:pts[i].tupler() for i in pts}
    labels = nx.get_edge_attributes(G,'weight')
    cmap = []
    for node in G:
        if node == home:
            cmap.append('r')
        elif node in tas:
            cmap.append('g')
        else:
            cmap.append('c')
    nx.draw_networkx_nodes(G, pos, node_color=cmap)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.savefig("libs/imgs/" + str(args.locations) + ".png")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize graphs.")
    parser.add_argument("files", type=str, help="*.in file or folder with *.in files")
    args = parser.parse_args()

    if os.path.isdir(args.files):
        for filename in sorted(glob.glob(args.files + "/*.in")):
            print("Displaying " + filename + "...")
            try:
                displayFile(filename)
            except:
                print("Done!")
                exit(0)
    else:
        print("Displaying " + args.files + "...")
        try:
            displayFile(args.files)
        except:
            print("Done!")
            exit(0)