import os, subprocess, argparse, shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Removes files entered from input folder")
    parser.add_argument("folder", type=str, help="Folder containing files to be entered (default: orgin)")
    args = parser.parse_args()

    print("Enter some files to copy from  {} (We'll just keep the basename)".format(args.folder))
    subprocess.run(["subl","-n", "-w","tmp.txt"])

    print("Thanks! Removing them now...")
    t = open("tmp.txt")
    for l in t.readlines():
        base = os.path.basename(l.strip())
        file = args.folder + "/" + base
        if os.path.isfile(file):
            print("Removed {}!".format(file))
            os.remove(file)
        else:
            print("File does not exist or is directory: " + file)
    t.close()

    os.remove("tmp.txt")

    print("Done!")