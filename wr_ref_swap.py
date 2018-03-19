import os
import sys
import argparse
import json

parser = argparse.ArgumentParser(description="Processes a Maya MA file, replacing paths using a JSON map")
parser.add_argument("-f",  "--file", dest="file", required=True, help="The Maya MA file to be processed")
parser.add_argument("-j", "--json", dest="json", required=True, help="The JSON Map file to use")
parser.add_argument("-o", "--output", dest="outfile", required=True, help="The MA file to output")

if __name__ == "__main__":
    args = parser.parse_args()
    # print args.file
    # print args.json
    # print args.outfile
    if not os.path.exists(os.path.expanduser(args.file)):
        sys.stderr.write("wr_ref_swap: input file {0} doesn't exist".format(args.file))
        exit(-1)
    if not os.path.exists(os.path.expanduser(args.json)):
        sys.stderr.write("wr_ref_swap: json file {0} doesn't exist".format(args.json))
        exit(-2)
    if not os.path.exists(os.path.dirname(args.outfile)):
        try:
            out_dir = os.path.dirname(args.outfile)
            if (out_dir != ""):
                os.mkdir(os.path.dirname(args.outfile))
        except Exception as e:
            sys.stderr.write(e)
            exit(-3)

    mapfile = open(os.path.expanduser(args.json), "r")

    mapping = json.load(mapfile)

    out_contents = str()

    with open(os.path.expanduser(args.file), "r") as mayafile:
        for line in mayafile:
            for key in mapping.keys():
                line = line.replace(key, mapping[key])
            out_contents += line

    with open(os.path.expanduser(args.outfile), "w") as out_file:
        out_file.write(out_contents)

    print("swap complete: old file{0}, mapping: {1},  new file{2}".format(args.file, args.json, args.outfile))
    exit(0)