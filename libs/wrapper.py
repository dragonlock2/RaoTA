import argparse, subprocess, sys, glob, os, datetime

def form(f):
	std = "{:4.2f}".format(f)
	if len(std) > 7:
		return "{:.1E}".format(f)
	return std

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Wraps the whole testing workflow in one simple script")
	parser.add_argument("-s", "--solver", default="algs/brutepython", type=str, help="Folder that contains solver.py for alg to use (default algs/brutepython)")
	parser.add_argument("-b", "--benchmark", action="store_true", help="If specified, runs existing input files (deletes naive and ignores other args)")
	parser.add_argument("-t", "--ta_frac", default=0.5, type=float, help="Fraction of total homes that have TAs in them (default 0.5)")
	parser.add_argument("-e", "--extra_edge_frac", default=0.5, type=float, help="Number of extra edges to add as a fraction of total nodes (default 0.5)")
	parser.add_argument("-n", "--nodes", default=[10], type=int, nargs="*", help="Number of nodes for each test case (default 10)")
	parser.add_argument("--archive", action="store_true", help="If specified, archives the input and output files")
	args = parser.parse_args()

	python = sys.executable

	if args.benchmark:
		# remove old naive files and outputs
		olds = glob.glob("libs/inputs/*naive*") + glob.glob("libs/outputs/*.out")
		if olds:
			subprocess.run(["rm", *olds])
		args.nodes = len(glob.glob("libs/inputs/*.in"))*[0]
		print()
	else:
		print("Deleting old inputs/outputs...", end="")
		sys.stdout.flush()
		subprocess.run(["rm libs/imgs/*.png"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		subprocess.run(["rm libs/inputs/*.in"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		subprocess.run(["rm libs/outputs/*.out"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print("Done!\n")

		print("Generating inputs... ", end="")
		sys.stdout.flush() # aiya didn't realize this before
		for n in args.nodes:
			subprocess.run([python, "libs/inputgen.py", "libs/inputs/" + str(n) + ".in", str(n), str(int(n*args.ta_frac)), str(int(n*args.extra_edge_frac)), "-v"])
		print("Done!\n")

		print("Validating inputs... ", end="")
		sys.stdout.flush()
		p = subprocess.run([python, "libs/input_validator.py", "--all", "libs/inputs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if len(p.stdout.split(b'\n')) > len(args.nodes) * 4 + 1:
			print("Uh-oh! Something bad happened :(")
			sys.exit(1)
		print("Done!\n")

	print("Solving inputs using " + args.solver + "...")
	subprocess.run([python, args.solver + "/solver.py", "--all", "libs/inputs", "libs/outputs"])
	print("Done!\n")

	print("Solving inputs naively... ", end="")
	sys.stdout.flush()
	subprocess.run([python, "libs/naivesolver.py"])
	print("Done!\n")

	print("Validating outputs...\n")
	sys.stdout.flush()
	p = subprocess.run([python, "libs/output_validator.py", "--all", "libs/inputs", "libs/outputs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	v = p.stdout.split(b'\n')
	v = [v[11*i:11*(i+1)] for i in range(2*len(args.nodes))]
	v.sort(key=lambda x:x[1])
	v = [(v[i], v[i+1]) for i in range(0, len(v), 2)]
	for o, n in v:
		d, w, t = float(o[7].split(b' ')[-1][:-1]), float(o[8].split(b' ')[-1][:-1]), float(o[9].split(b' ')[-1][:-1])
		algt = t
		d, w, t = form(d), form(w), form(t)
		print(o[1].decode("utf-8").split(" ")[1] + "     ", "Drive:", d, "Walk:", w, "Total:", t, sep='\t')

		d, w, t = float(n[7].split(b' ')[-1][:-1]), float(n[8].split(b' ')[-1][:-1]), float(n[9].split(b' ')[-1][:-1])
		naivet = t
		d, w, t = form(d), form(w), form(t)
		print(n[1].decode("utf-8").split(" ")[1], "Drive:", d, "Walk:", w, "Total:", t, sep='\t')

		print("Percent improvement over naive:", round((naivet-algt)/naivet*100, 3),"\b%")

		print()
		
	print("Done!\n")

	# delete naive files to avoid clutter
	naives = glob.glob("libs/inputs/*naive*") + glob.glob("libs/outputs/*naive*")
	if naives:
		subprocess.run(["rm", *naives])

	if args.archive:
		print("Archiving input and output files...", end="")
		sys.stdout.flush()

		subprocess.run([python, "libs/archive.py", args.solver])

		print("Done!\n")





