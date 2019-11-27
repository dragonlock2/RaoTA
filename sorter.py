import sys, glob, subprocess, argparse, os, shutil
sys.path.append("libs/")
import input_validator as iv

EX_CUT = 0.25
foldernames = ["50", "100", "200", "other", "bruteforceable"]

def getAttrs(filename):
    input_data = iv.utils.read_file(filename)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = iv.data_parser(input_data)
    G, _ = iv.adjacency_matrix_to_graph(adjacency_matrix)
    exedge = G.number_of_edges() - num_of_locations + 1 # how many extra edges on top of a tree
    exfrac = exedge / (num_of_locations**2) # not the exact frac, but close enough
    return num_of_locations, num_houses, exfrac

def moveFile(filename, folder, exfrac, excut=EX_CUT):
    if exfrac <= EX_CUT:
        shutil.move(filename, folder + "/treeish")
        os.mkdir(folder + "/treeish/" + f[:-3])
    else:
        shutil.move(filename, folder + "/tspable")
        os.mkdir(folder + "/tspable/" + f[:-3])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sorts input folder into output folder")
    parser.add_argument("-i", "--infolder",default="inputs/", type=str, help="Folder with *.in files")
    parser.add_argument("-o", "--outfolder", default="orginout/", type=str, help="Folder to sort into")
    args = parser.parse_args()

    print("Removing old files in {}. ".format(args.outfolder), end="")
    input("Press enter to continue...")
    shutil.rmtree(args.outfolder)
    os.mkdir(args.outfolder)
    for f in glob.glob(args.infolder + "/*.in"):
        shutil.copy(f, args.outfolder)

    # Sort by size and completeness
    print("Sorting by size and completeness...")
    os.chdir(args.outfolder)
    for fn in foldernames:
        os.mkdir(fn)
        os.mkdir(fn + "/tspable")
        os.mkdir(fn + "/treeish")

    for f in glob.glob("*.in"):
        numlocs, numtas, exfrac = getAttrs(f)
        if numlocs == 50 and numtas == 25:
            moveFile(f, "50", exfrac)
        elif numlocs == 100 and numtas == 50:
            moveFile(f, "100", exfrac)
        elif numlocs == 200 and numtas == 100:
            moveFile(f, "200", exfrac)
        elif numtas <= 12:
            moveFile(f, "bruteforceable", exfrac, 0.6)
        else:
            moveFile(f, "other", exfrac)









