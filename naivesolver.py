import glob, subprocess

# delete old naive files first
naives = glob.glob("./inputs/*naive*") + glob.glob("./outputs/*naive*")
if naives:
	subprocess.run(["rm", *naives])

for filename in glob.glob("inputs/*.in"):
	# read file
	f = open(filename, 'r')

	l = f.readlines()
	home, dropoffs = l[4], l[4][:-1] + " " + l[3]

	f.close()

	# copy file
	subprocess.run(["cp", filename, filename[:-3] + "naive.in"])

	# write file
	name = filename.split("/")[1][:-3]
	f = open("outputs/" + name + "naive.out", 'w')

	f.write(home)
	f.write("1\n")
	f.write(dropoffs)

	f.close()