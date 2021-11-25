#!/usr/bin/env python3
import getopt, sys, os
os.environ["FLASK_ENV"] = "development"
# order is important: be.server needs the FLASK_ENV set as above
sys.path.append(os.path.abspath('..'))
from be.tile_creator_2.main import main
from be.configuration import CONFIGURATIONS, data_folder
from be.server import SessionLocal
from be.server.gallery_categories.service import GalleryCategoryService

# def getCwd():
#     thisFileDir = os.path.dirname(os.path.realpath(__file__))
#     return thisFileDir

# if os.getcwd().split(os.sep)[-1] == "commands":
#     # if it's run from the commands frolder then chdire to be in root
#     os.chdir(os.path.abspath(".."))


def extract_cmd_arguments():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "n:z:"
    long_options = ["csv=", "ts=", "min_t=", "max_t=", "std=", "med_thick=", "max_thick=", "med_size=",
                    "max_size=", "curvature=", "mean_t=", "gc=", "bg_color=", "description="]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
        print("Extracted arguments: ", arguments)
    except getopt.error as err:
        print("GTM failed while parsing the arguments: " + str(err))
        sys.exit(2)
    return dict(arguments)


def get_final_configurations(raw_args, graph_name, category_id, description):
    defaults = CONFIGURATIONS['defaults']
    return {
        'graph_name': graph_name,
        "graph_category": category_id,
        "source": raw_args['--csv'],
        "tile_size": int(raw_args.get('--ts', defaults['tile_size'])),
        "zoom_levels": int(raw_args.get('-z', defaults['zoom_levels'])),
        "min_transparency": float(raw_args.get('--min_t', 0)),
        "max_transparency": float(raw_args.get('--max_t', 0.1)),
        "tile_based_mean_transparency": float(raw_args.get('--mean_t', defaults['tile_based_mean_transparency'])),
        "std_transparency_as_percentage": float(raw_args.get("--std", defaults["std_transparency_as_percentage"])),
        "max_edge_thickness": float(raw_args.get('--max_thick', defaults["max_edge_thickness"])),
        "med_edge_thickness": float(raw_args.get('--med_thick', defaults["med_edge_thickness"])),
        "max_vertex_size": float(raw_args.get("--max_size", defaults["max_vertex_size"])),
        "med_vertex_size": float(raw_args.get("--med_size", defaults["med_vertex_size"])),
        "curvature": float(raw_args.get("--curvature", defaults['edge_curvature'])),
        "bg_color": raw_args.get("--bg_color", defaults['bg_color']),
        "description": description
    }


def resolve_graph_category(raw_args):
    with SessionLocal() as db:
        categories = GalleryCategoryService.get_all(db)
        category_id = next(filter(lambda cat: cat.title == raw_args.get("--gc", 'default'), categories)).id
        return category_id


def format_graph_name(raw_args):
    graph_name = raw_args["-n"].lower().strip()
    graph_name = '_'.join(graph_name.split(' '))
    return graph_name


def read_description_file(description_file):
    if description_file == None:
        return ''
    with open(description_file, 'r') as f:
        return f.readlines()


if __name__ == "__main__":
    raw_args = extract_cmd_arguments()

    print("%-40s %s" % ("PROCESSING STEP", "TIME"))

    graph_category_id = resolve_graph_category(raw_args)
    graph_name = format_graph_name(raw_args)

    description = read_description_file(
        raw_args.get(
            "--description",
            os.path.join(data_folder, "default_description.html")
        )
    )
    description = "".join(description)

    configurations = get_final_configurations(raw_args, graph_name, graph_category_id, description)

    main(configurations)

    print("gtm finished!")
