import sys, glob, subprocess, argparse
sys.path.append("libs/")
import output_validator as ov

def get_costs(infile, outfile): # driving, walking, total
	indat = ov.utils.read_file(infile)
	outdat = ov.utils.read_file(outfile)
	cost, msg = ov.tests(indat, outdat)
	return [float(s.split(" ")[-1][:-1]) for s in msg.split('\n')[:-1]]

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Records characteristics of optimal solutions.")
	parser.add_argument("-f", "--file", default="benchmark.csv", type=str, help="File to append to")
	parser.add_argument("trials", type=int, help="Number of trials per case")
	parser.add_argument("nodes", type=int, help="Number of nodes to test")
	parser.add_argument("edge_min", type=int, help="Smallest extra number of edges (multiplicative factor)")
	parser.add_argument("edge_max", type=int, help="Largest extra number of edges (max=nodes)")
	parser.add_argument("edge_step", type=int, help="Step for extra number of edges")
	args = parser.parse_args()

	if (args.nodes > 32):
		print("Too many nodes!")
		exit(1)

	f = open(args.file, "a+")

	for e in range(args.edge_min, args.edge_max+1, args.edge_step):
		for i in range(args.trials):
			print("Nodes: {} Edges: {} Trial: {}...".format(args.nodes, e, i), end="")
			sys.stdout.flush()
			subprocess.run(["python3", "libs/inputgen.py", "libs/inputs/test.in", str(args.nodes), str(int(0.5*args.nodes)), str(int(e*args.nodes))])


			subprocess.run(["python3", "algs/brutecppLVIII/solver.py", "libs/inputs/test.in", "libs/outputs/"], stdout=subprocess.PIPE)
			subprocess.run(["python3", "libs/naivesolver.py"])

			d, w, t = get_costs("libs/inputs/test.in", "libs/outputs/test.out")
			nd, nw, nt = get_costs("libs/inputs/testnaive.in", "libs/outputs/testnaive.out")

			# <# nodes>, <mult extra edges>, <% improvement over naive>, <% driving cost>
			a = [args.nodes, e, round((nt-t)/nt*100, 2), round(d/t*100, 2)]
			f.write(",".join([str(i) for i in a]) + "\n")

			subprocess.run("rm libs/inputs/*naive* libs/outputs/*naive*", shell=True)
			subprocess.run("rm libs/inputs/test.in libs/outputs/test.out", shell=True)
			print(" done!")


	f.close()