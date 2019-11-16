import argparse, subprocess, sys, glob

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate some inputs")
	parser.add_argument("-b", "--benchmark", action="store_true", help="If specified, runs existing input files (deletes naive and ignores other args)")
	parser.add_argument("-t", "--ta_frac", default=0.5, type=float, help="Fraction of total homes that have TAs in them (default 0.5)")
	parser.add_argument("-e", "--extra_edge_frac", default=0.5, type=float, help="Number of extra edges to add as a fraction of total nodes (default 0.5)")
	parser.add_argument("-n", "--nodes", default=[10], type=int, nargs="*", help="Number of nodes for each test case (default 10)")
	args = parser.parse_args()

	python = sys.executable

	if args.benchmark:
		# remove old naive files and outputs
		olds = glob.glob("./inputs/*naive*") + glob.glob("./outputs/*.out")
		if olds:
			subprocess.run(["rm", *olds])
		args.nodes = len(glob.glob("./inputs/*.in"))*[0]
		print()
	else:
		print("Deleting old inputs/outputs...", end="")
		sys.stdout.flush()
		subprocess.run(["rm inputs/*.in"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		subprocess.run(["rm outputs/*.out"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print("Done!\n")

		print("Generating inputs... ", end="")
		sys.stdout.flush() # aiya didn't realize this before
		for n in args.nodes:
			subprocess.run([python, "inputgen.py", "inputs/" + str(n) + ".in", str(n), str(round(n*args.ta_frac)), str(round(n*args.extra_edge_frac))])
		print("Done!\n")

		print("Validating inputs... ", end="")
		sys.stdout.flush()
		p = subprocess.run([python, "input_validator.py", "--all", "inputs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if len(p.stdout.split(b'\n')) > len(args.nodes) * 4 + 1:
			print("Uh-oh! Something bad happened :(")
			sys.exit(1)
		print("Done!\n")

	print("Solving inputs... ")
	subprocess.run([python, "solver.py", "--all", "inputs", "outputs"])
	print("Done!\n")

	print("Solving inputs naively... ", end="")
	sys.stdout.flush()
	subprocess.run([python, "naivesolver.py"])
	print("Done!\n")

	print("Validating outputs...\n")
	sys.stdout.flush()
	p = subprocess.run([python, "output_validator.py", "--all", "inputs", "outputs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	v = p.stdout.split(b'\n')
	v = [v[11*i:11*(i+1)] for i in range(2*len(args.nodes))]
	v.sort(key=lambda x:x[1])
	v = [(v[i], v[i+1]) for i in range(0, len(v), 2)]
	for o, n in v:
		d, w, t = round(float(o[7].split(b' ')[-1][:-1]), 3), round(float(o[8].split(b' ')[-1][:-1]), 3), round(float(o[9].split(b' ')[-1][:-1]), 3)
		print(o[1].decode("utf-8").split(" ")[1] + "     ", "Drive:", d, "Walk:", w, "Total:", t, sep='\t')
		d, w, t = round(float(n[7].split(b' ')[-1][:-1]), 3), round(float(n[8].split(b' ')[-1][:-1]), 3), round(float(n[9].split(b' ')[-1][:-1]), 3)
		print(n[1].decode("utf-8").split(" ")[1], "Drive:", d, "Walk:", w, "Total:", t, sep='\t')
		print()
		
	print("Done!\n")

	# delete naive files to avoid clutter
	naives = glob.glob("./inputs/*naive*") + glob.glob("./outputs/*naive*")
	if naives:
		subprocess.run(["rm", *naives])





