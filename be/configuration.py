import json
import multiprocessing
import os

this_file_dir = os.path.dirname(os.path.realpath(__file__))
data_folder = os.path.join(this_file_dir, '../data')

AVAILABLE_CORES = multiprocessing.cpu_count()
# print(f'{AVAILABLE_CORES} cores were detected on your system')
MAX_CORES = AVAILABLE_CORES - 2  # the parallelization will use at most (AVAILABLE_CORES - CORES_UNUSED) cores

# DB CONFIGURATIONS
DB_USER_NAME = 'tokengallerist'
DB_PASSWORD = '1234'
DB_URL = '127.0.0.1'
DB_NAME = 'tg_main'
VERTEX_GLOBAL_TABLE = 'tg_vertex'
EDGE_GLOBAL_TABLE = 'tg_edge'
VERTEX_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_vertex"
EDGE_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_edge"
TILE_FOLDER_NAME = lambda graph_id: f'tiles_graph_{graph_id}'
USER_TABLE = 'tg_user'
VERTEX_METADATA_TABLE = "tg_vertex_metadata"

LABELS_TABLE = 'tg_labels'
LABELS_TABLE_ETH = 'eth'
LABELS_TABLE_LABEL = 'label'
LABELS_TABLE_TYPE = 'type'

# GIS CONFIGURATIONS
SRID = 3857

FA2_OPTIONS = {'max_iter': 500,
                             'strong_gravity_mode': True,
                             'barnes_hut_theta': 1.2,
                             'outbound_attraction_distribution': False,
                             'gravity': 1,
                             'scaling_ratio': 1}

def load_configurations():
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)


CONFIGURATIONS = load_configurations()

def internal_id(source_or_target):
    if source_or_target == "source":
        return 'source_' + CONFIGURATIONS['vertex_internal_id']
    if source_or_target == "target":
        return 'target_' + CONFIGURATIONS['vertex_internal_id']

def external_id(source_or_target):
    if source_or_target == "source":
        return 'source_' + CONFIGURATIONS['vertex_external_id']
    if source_or_target == "target":
        return 'target_' + CONFIGURATIONS['vertex_external_id']
