#!/usr/bin/env python3
import getopt, sys, os
os.environ["FLASK_ENV"] = "development"
# order is important: be.server needs the FLASK_ENV set as above
sys.path.append(os.path.abspath('..'))
from be.configuration import CONFIGURATIONS
from be.server import SessionLocal
from be.server.gallery_categories.service import GalleryCategoryService
from be.tile_creator.main import main

if os.getcwd().split(os.sep)[-1] == "commands":
    # if it's run from the commands frolder then chdire to be in root
    os.chdir(os.path.abspath(".."))


def extractArguments():
    global arguments, values
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    print(argumentList)
    shortOptions = "n:z:"
    longOptions = ["csv=", "ts=", "min_t=", "max_t=", "std=", "med_thick=", "max_thick=", "med_size=",
                   "max_size=", "curvature=", "mean_t=", "gc="]
    try:
        arguments, values = getopt.getopt(argumentList, shortOptions, longOptions)
        print(">>> ", arguments)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)
    return dict(arguments)


def getCwd():
    thisFileDir = os.path.dirname(os.path.realpath(__file__))
    return thisFileDir


# default value as second arg of 'get'
# TODO find a way of ensuring that htis dict keys are the same as defined in configuration.json
def getFinalConfigurations(args, graph_name, category_id):
    configurations = {
        'graph_name': graph_name,
        "tile_size": int(args.get('--ts', CONFIGURATIONS['tile_size'])),
        "zoom_levels": int(args.get('-z', 2)),
        "min_transparency": float(args.get('--min_t', 0)),
        "max_transparency": float(args.get('--max_t', 0.1)),
        "tile_based_mean_transparency": float(args.get('--mean_t', 0.5)),
        "std_transparency_as_percentage": float(args.get("--std", 0.25)),
        "max_edge_thickness": float(args.get('--max_thick', 2)),
        "med_edge_thickness": float(args.get('--med_thick', 0.25)),
        "max_vertex_size": float(args.get("--max_size", 10)),
        "med_vertex_size": float(args.get("--med_size", 0.5)),
        "curvature": float(args.get("--curvature", CONFIGURATIONS['edge_curvature'])),
        "graph_category": category_id,
        "bg_color": "grey",
        "source": args['--csv']
    }
    return configurations


if __name__ == "__main__":
    args = extractArguments()

    # resolve gallery category with categories in db
    with SessionLocal() as db:
        categories = GalleryCategoryService.get_all(db)
        category_id = next(filter(lambda cat: cat.title == args.get("--gc", 'default'), categories)).id

    # graph names should be lower case and don't contain spaces
    graph_name = args["-n"].lower().strip()
    graph_name = '_'.join(graph_name.split(' '))

    configurations = getFinalConfigurations(args, graph_name, category_id)
    main(configurations)
