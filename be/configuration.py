import os
import json

this_file_dir = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(this_file_dir, 'data')

LARGE_GRAPH_RAW_PATH = os.path.join(data_folder, 'large.csv')
MEDIUM_GRAPH_RAW_PATH = os.path.join(data_folder, 'medium.csv')
SMALL_GRAPH_RAW_PATH = os.path.join(data_folder, 'small.csv')
MOCK_LABELLED_RAW_PATH = os.path.join(data_folder, 'mock_net_labelled.csv')
LABELS_PATH = os.path.join(data_folder, 'etherscanLabels20200529.csv')
METADATA_PATH = os.path.join(data_folder, 'metadata.csv')
MIN_MAX_PATH = os.path.join(data_folder, 'min_max.csv')

def _load_configurations():
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)


CONFIGURATIONS = _load_configurations()
