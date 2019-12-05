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
    f = open("temp/naive.out", 'w')
    f.write(home)
    f.write("1\n")
    f.write(dropoffs)
    f.close()
    _, _, nt = get_costs(infile, "temp/naive.out")
    subprocess.run("rm temp/naive.out", shell=True)
    return nt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves inputs using specified algorithm and replaces the file in outputs if it's better.")
    parser.add_argument("solver", type=str, help="Folder containing solver.py for algorithm to be used")
    parser.add_argument("inputs", type=str, help="Folder with *.in files")
    parser.add_argument("outputs", type=str, help="Folder to output into")
    parser.add_argument("-l", "--long", action="store_true", help="If specified runs from orgin/long folder and disables timeout")
    parser.add_argument("-t", "--timeout", default=120, type=float, help="Specifies max time each input file will have to finish (Default: 60s)")
    parser.add_argument("-g", "--debug", action="store_true", help="If specified, will not delete temp/ folder after finishing and disables timeout")
    args = parser.parse_args()

    python = sys.executable # To make easier to run different versions

    if args.long:
        args.inputs = "orgin/long"
        args.timeout = 86400 # can't really pass in too big number into timeout
    else:
        print("Removing orgin/long...")
        if os.path.isdir("orgin/long"):
            shutil.rmtree("orgin/long")
        os.mkdir("orgin/long")
    long_flag = False

    if not os.path.isdir("temp"):
        os.mkdir("temp")

    print("Using {}...".format(args.solver))
    print("Solving from {}...".format(args.inputs))
    for f in glob.glob(args.inputs + "/*.in"):
        print("Solving {}...".format(os.path.basename(f)), end="")
        sys.stdout.flush()

        try:
            t0 = time.perf_counter()
            if args.debug:
                subprocess.run([python, args.solver + "/solver.py", f, "temp"])
            else:
                subprocess.run([python, args.solver + "/solver.py", f, "temp"], stdout=subprocess.PIPE, timeout=args.timeout)
            t1 = time.perf_counter()

            print("{}s! ".format(round(t1-t0,2)), end="")
            sys.stdout.flush()

            outfile = os.path.splitext(os.path.basename(f))[0] + ".out"
            oldfile = args.outputs + "/" + outfile
            _, _, t = get_costs(f, "temp/" + outfile)
            nt = get_naive(f)
            ot = get_costs(f, oldfile)[2] if os.path.exists(oldfile) else float('inf')
            print("new: {}% old: {}%".format(round((nt-t)/nt*100,2), round((nt-ot)/nt*100, 2)), end="")
            if (t < ot):
                print(" Yeet!")
                if os.path.exists(oldfile):
                    os.remove(oldfile)
                shutil.copyfile("temp/" + outfile, oldfile)
            else:
                print()
        except subprocess.TimeoutExpired:
            # little hack to automate appending to optimal.md
            opmd = open("optimal.md", "a")
            opmd.write(f[6:] + "\n")
            opmd.close()

            long_flag = True
            shutil.copyfile(f, "orgin/long/" + os.path.basename(f))
            print(" took too long! (copied to orgin/long)")

    if not long_flag:
        shutil.rmtree("orgin/long")
    else:
        print("Rerun with -l flag to run on orgin/folder (also disables timeout)")

    if not args.debug:
        shutil.rmtree("temp/")


