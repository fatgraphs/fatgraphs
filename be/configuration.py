import os
import json

this_file_dir = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(this_file_dir, 'data')

TILE_SOURCE = os.path.join(this_file_dir, 'tiles')
MEDIUM_GRAPH_RAW_PATH = os.path.join(data_folder, 'medium.csv')
BG_COLOR = 'black'


def _load_configurations():
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)


CONFIGURATIONS = _load_configurations()
