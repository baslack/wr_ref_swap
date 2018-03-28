import os
import sys
import argparse
import json
import copy
import re

def parse_line(config, ln):
    '''

    :param config:
    :type config: dict
    :param ln:
    :type ln: str
    :return:
    :rtype: str
    '''
    # file -rdi 1 -ns "Martin" -rfn "MartinRN" -typ "mayaAscii" "$ART_LOCAL_ROOT/_art/production/2/23c81e21-5c4c-4481-b24c-3918fd10499e/Assets/Characters/Martin/__model_v022__/model/Martin.ma";
    # file -r -ns "Martin" -dr 1 -rfn "MartinRN" -typ "mayaAscii" "$ART_LOCAL_ROOT/_art/production/2/23c81e21-5c4c-4481-b24c-3918fd10499e/Assets/Characters/Martin/__model_v022__/model/Martin.ma";

    tokens = ln.split(" ")
    # firsts determine if we're dealing with a "file" line for references
    if "file" in tokens:
        pass
    else:
        return ln;
        tokens.index("file")
    # next, find the path token in the file line
    for token in tokens:
        # the path token
        if not (token.find("ART_LOCAL_ROOT") < 0):
            # found the path token
            path_raw = copy.deepcopy(token)
            path_raw = path_raw.lstrip("\"")
            path_raw = path_raw.rstrip("\";\n")
            path_tokens = path_raw.split("/")

            # sanity check, are we looking at something from our project
            if config["project-id"] not in path_tokens:
                return ln

            asset_name = path_tokens[path_tokens.index("Assets")+2]

            bMap = False
            try:
                if asset_name in config["map"].keys():
                    # perform a map
                    # is the map rig installed?
                    asset_path = os.path.abspath(config["ART_LOCAL_ROOT"])
                    for i in range(1, path_tokens.index("Assets") + 2):
                        asset_path = os.path.join(asset_path, path_tokens[i])
                    if not os.path.exists(asset_path):
                        raise IOError("asset path doesn't exist")
                    # directory list of asset sub directory
                    installed_assets = os.listdir(asset_path)
                    if config["map"][asset_name] in installed_assets:
                        # replace the asset path
                        path_tokens[path_tokens.index("Assets") + 2] = config["map"][asset_name]
                        # replace the filename
                        path_tokens[-1] = config["file"][config["map"][asset_name]]
                        bMap = True
            except KeyError:
                pass

            asset_name = path_tokens[path_tokens.index("Assets")+2]

            bUpdate = False
            try:
                if asset_name in config["update"]:
                    # perform an update
                    asset_path = os.path.abspath(config["ART_LOCAL_ROOT"])
                    for i in range(1, path_tokens.index("Assets") + 3):
                        asset_path = os.path.join(asset_path, path_tokens[i])
                    if not os.path.exists(asset_path):
                        raise IOError("asset path doesn't exist")
                    # directory list of asset sub directory
                    installed_version_dirs = os.listdir(asset_path)
                    regex = re.compile("__[a-zA-Z0-9]+_*[a-zA-Z0-9]*_v([0-9]+)__")
                    installed_versions = list()
                    for version_dir in installed_version_dirs:
                        if regex.match(version_dir):
                            installed_versions.append(int(regex.match(version_dir).groups()[0]))
                    if not len(installed_versions) == 0:
                        highest_version = max(installed_versions)
                        highest_version_dir = installed_version_dirs[installed_versions.index(highest_version)]
                        path_tokens[path_tokens.index("Assets") + 3] = highest_version_dir
                        bUpdate = True
            except KeyError:
                pass

            # we made not changes, just return the line
            if not(bMap or bUpdate):
                return ln

            # we made changes, put the changes back
            new_path = "\""
            for path_token in path_tokens:
                new_path += (path_token + "/")
            new_path = new_path.rstrip("/")
            new_path += "\";\n"
            tokens[tokens.index(token)] = new_path

    new_line = ""
    for token in tokens:
        new_line += (token + " ")
    new_line.rstrip(" ")
    return new_line

# TODO : add arguments for command line spec of some JSON options

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

    # mapping = json.load(mapfile)

    config = json.load(mapfile)

    out_contents = str()

    with open(os.path.expanduser(args.file), "r") as mayafile:
        for line in mayafile:
            # for key in mapping.keys():
            #     line = line.replace(key, mapping[key])
            line = parse_line(config, line)
            out_contents += line

    with open(os.path.expanduser(args.outfile), "w") as out_file:
        out_file.write(out_contents)

    print("swap complete: old file{0}, mapping: {1},  new file{2}".format(args.file, args.json, args.outfile))
    exit(0)