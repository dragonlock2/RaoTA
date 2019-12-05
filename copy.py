import os, subprocess, argparse, shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copies files in a text file over from one folder to another")
    parser.add_argument("-i", "--infolder", default="orgin", type=str, help="Folder containing files to be entered (default: orgin)")
    parser.add_argument("-o", "--outfolder", default="tmplong", type=str, help="Folder to write files to (default: tmplong")
    parser.add_argument("-r", "--remove", action="store_true", help="If specified, will also remove all files in outfolder")
    args = parser.parse_args()

    if args.remove:
        print("Removing old files...")
        if os.path.isdir(args.outfolder):
            shutil.rmtree(args.outfolder)
        os.mkdir(args.outfolder)

    if not os.path.isdir(args.outfolder):
        print("Making output folder...")
        os.mkdir(args.outfolder)

    print("Enter some files to copy...")
    subprocess.run(["subl","-n", "-w","tmp.txt"])

    print("Thanks! Copying them over now...")
    t = open("tmp.txt")
    for l in t.readlines():
    	l = l.strip()
    	shutil.copyfile(args.infolder + "/" + l, args.outfolder + "/" + os.path.basename(l))
    t.close()

    os.remove("tmp.txt")

    print("Done!")