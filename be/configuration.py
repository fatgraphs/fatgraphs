import multiprocessing
import os
import json

this_file_dir = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(this_file_dir, 'data')

AVAILABLE_CORES = multiprocessing.cpu_count()
# print(f'{AVAILABLE_CORES} cores were detected on your system')
MAX_CORES = AVAILABLE_CORES - 2  # the parallelization will use at most (AVAILABLE_CORES - CORES_UNUSED) cores

# DB CONFIGURATIONS
DB_USER_NAME = 'postgres'
DB_PASSWORD = '1234'
DB_URL = '127.0.0.1'
DB_NAME = 'test'
VERTEX_GLOBAL_TABLE = 'tg_vertex'
VERTEX_TABLE_NAME = lambda graph_name, graph_id: f"{graph_name}_{graph_id}"
USER_TABLE = 'tg_user'
VERTEX_METADATA_TABLE = "tg_vertex_metadata"

LABELS_TABLE = 'tg_labels'
LABELS_TABLE_ETH = 'eth'
LABELS_TABLE_LABEL = 'label'
LABELS_TABLE_TYPE = 'type'


#GIS CONFIGURATIONS
SRID = 3857

def load_configurations():
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)


CONFIGURATIONS = load_configurations()
