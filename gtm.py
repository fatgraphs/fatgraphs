#!/usr/bin/env python
import getopt, sys, os


# -n "experiment number 7" -csv="path/to/file" -ts=512 -z=3 -min_t=0.01 -max_t=0.1 -std=0.5 -max_edge_thickness=8 -min_edge_thickness=1
from be.tile_creator.main import main


def extract_arguments():
    global arguments, values
    # Get full command-line arguments
    full_cmd_arguments = sys.argv
    # Keep all but the first
    argument_list = full_cmd_arguments[1:]
    print(argument_list)
    short_options = "n:z:"
    long_options = ["csv=", "ts=", "min_t=", "max_t=", "std=", "min_thick=", "max_thick="]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)
    return dict(arguments)


def get_cwd():
    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    return this_file_dir


def result_in_directory_existing(path):
    if not os.path.exists(path):
        os.mkdir(path)




def ensure_container_directory_exists():
    result_in_directory_existing(os.path.join(get_cwd(), "graph-maps"))




def mkdir_for_this_graph():
    path = os.path.join(get_cwd(), "graph-maps")
    path = os.path.join(path, args["-n"])
    result_in_directory_existing(path)
    return path


args = extract_arguments()
ensure_container_directory_exists()
graph_path = mkdir_for_this_graph()

# default value as second arg og 'get'
# TODO find a way of ensuring that htis dict keys are the same as defined in configuration.json
configurations = {
    "output_folder": graph_path,
    "tile_size": args.get('-ts', 512),
    "zoom_levels": int(args.get('-z', 2)),
    "min_transparency": args.get('-min_t', 0.01),
    "max_transparency": args.get('-max_t', 0.1),
    "std_transparency_as_percentage": args.get("-std", 0.5),
    "max_edge_thickness": args.get('-min_thick', 1),
    "min_edge_thickness": args.get('-max_thick', 8),
    "bg_color": "black"
}

main(args['--csv'], configurations)

# # Evaluate given options
# for current_argument, current_value in arguments:
#     if current_argument in ("-v", "--verbose"):
#         print("Enabling verbose mode")
#     elif current_argument in ("-h", "--help"):
#         print("Displaying help")
#     elif current_argument in ("-o", "--output"):
#         print(("Enabling special output mode (%s)") % (current_value))
