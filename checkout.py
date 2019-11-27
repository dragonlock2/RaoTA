import glob, os

if __name__ == "__main__":
	print("Checking what inputs we haven't solved yet...")

	count = 0

	for f in glob.glob("inputs/*.in"):
		outfile = "outputs/" + os.path.splitext(os.path.basename(f))[0] + ".out"
		if not os.path.exists(outfile):
			print(f)
			count += 1

	print("{} files".format(count))
