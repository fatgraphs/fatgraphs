import os
import json

this_file_dir = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(this_file_dir, 'data')

LARGE_GRAPH_RAW_PATH = os.path.join(data_folder, 'large.csv')
MEDIUM_GRAPH_RAW_PATH = os.path.join(data_folder, 'medium.csv')
SMALL_GRAPH_RAW_PATH = os.path.join(data_folder, 'small.csv')
MOCK_LABELLED_RAW_PATH = os.path.join(data_folder, 'mock_net_labelled.csv')
LABELS_PATH = os.path.join(data_folder, 'labels.csv')

# DB CONFIGURATIONS
DB_USER_NAME = 'postgres'
DB_PASSWORD = '1234'
DB_URL = '127.0.0.1'
DB_NAME = 'test'
METADATA_TABLE_NAME = lambda graph_name: graph_name + "_metadata"
ID_TABLE_NAME = lambda graph_name: graph_name + "_id"
VERTEX_TABLE_NAME = lambda graph_name: graph_name + "_vertex"

#GIS CONFIGURATIONS
SRID = 3857

def _load_configurations():
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)


CONFIGURATIONS = _load_configurations()
