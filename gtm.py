#!/usr/bin/env python
import getopt, sys, os

# -n "experiment number 7" -csv="path/to/file" -ts=512 -z=3 -min_t=0.01 -max_t=0.1 -std=0.5 -max_edge_thickness=8 -min_edge_thickness=1
from be.configuration import CONFIGURATIONS
from be.tile_creator.main import main


def extractArguments():
    global arguments, values
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    print(argumentList)
    shortOptions = "n:z:"
    longOptions = ["csv=", "labels=", "ts=", "min_t=", "max_t=", "std=", "med_thick=", "max_thick=", "med_size=",
                    "max_size=", "curvature=", "mean_t="]
    try:
        arguments, values = getopt.getopt(argumentList, shortOptions, longOptions)
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
def getFinalConfigurations(args, graph_name):
    configurations = {
        'graphName': graph_name,
        "tileSize": int(args.get('--ts', 256)),
        "zoomLevels": int(args.get('-z', 2)),
        "minTransparency": float(args.get('--minT', 0)),
        "maxTransparency": float(args.get('--maxT', 0.1)),
        "tileBasedMeanTransparency": float(args.get('--meanT', 0.5)),
        "stdTransparencyAsPercentage": float(args.get("--std", 0.25)),
        "maxEdgeThickness": float(args.get('--maxThick', 2)),
        "medEdgeThickness": float(args.get('--medThick', 0.25)),
        "maxVertexSize": float(args.get("--maxSize", 10)),
        "medVertexSize": float(args.get("--medSize", 0.5)),
        "curvature": float(args.get("--curvature", 0.1)),
        "bgColor": "black",
        "source": args['--csv'],
        "labels": args.get('--labels', None)
    }
    return configurations


if __name__ == "__main__":
    args = extractArguments()

    # graph names should be lower case and don't contain spaces
    graph_name = args["-n"].lower().strip()
    graph_name = '_'.join(graph_name.split(' '))

    configurations = getFinalConfigurations(args, graph_name)
    main(configurations)
