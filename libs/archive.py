import argparse, sys, os, subprocess, glob, datetime

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Archive files currently in libs/inputs/ and libs/outputs/")
	parser.add_argument("solver", type=str, help="Folder for algorithm that was used")
	args = parser.parse_args()

	pref = os.path.basename(os.path.abspath(args.solver)) + datetime.datetime.now().strftime("_%m-%d-%Y_%H%M%S_")
	for f in glob.glob("libs/inputs/*.in"):
		newname = pref + os.path.basename(f)
		subprocess.run(["cp", f, "libs/archive-inputs/"+newname])
	for f in glob.glob("libs/outputs/*.out"):
		newname = pref + os.path.basename(f)
		subprocess.run(["cp", f, "libs/archive-outputs/"+newname])

