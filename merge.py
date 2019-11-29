import sys, glob, subprocess, argparse, os, shutil, time
sys.path.append("libs/")
import output_validator as ov

def get_costs(infile, outfile): # driving, walking, total
    indat = ov.utils.read_file(infile)
    outdat = ov.utils.read_file(outfile)
    cost, msg = ov.tests(indat, outdat)
    return [float(s.split(" ")[-1][:-1]) for s in msg.split('\n')[:-1]]

def get_naive(infile):
    # read file
    f = open(infile)
    l = f.readlines()
    home, dropoffs = l[4], l[4][:-1] + " " + l[3]
    f.close()
    # write file
    name = infile.split("/")[-1][:-3]
    f = open("naive.out", 'w')
    f.write(home)
    f.write("1\n")
    f.write(dropoffs)
    f.close()
    _, _, nt = get_costs(infile, "naive.out")
    subprocess.run("rm naive.out", shell=True)
    return nt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace outputs in old_outputs with ones in new_outputs if they are better")
    parser.add_argument("new_outputs", type=str, help="Folder with .out files that might be better")
    parser.add_argument("old_outputs", type=str, help="Folder with .out files to be replaced")
    args = parser.parse_args()

    print("Let's merge!")

    for newout in glob.glob(args.new_outputs + "/*.out"):
        print("Trying {}...".format(newout), end="")
        sys.stdout.flush()
        infile = "inputs/" + os.path.splitext(os.path.basename(newout))[0] + ".in"
        oldout = args.old_outputs + "/" + os.path.basename(newout)

        _, _, newtot = get_costs(infile, newout)
        naivetot = get_naive(infile)
        oldtot = get_costs(infile, oldout)[2] if os.path.exists(oldout) else float('inf')
        print("new: {}% old: {}%".format(round((naivetot-newtot)/naivetot*100,2), round((naivetot-oldtot)/naivetot*100, 2)), end="")

        if newtot < oldtot:
            print("Yeet!")
            if os.path.exists(oldout):
                os.remove(oldout)
            shutil.copyfile(newout, oldout)
        else:
            print()
        
