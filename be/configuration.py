import json
import multiprocessing
import os

# ALL below are only used by tile creator or some commands

this_file_dir = os.path.dirname(os.path.realpath(__file__))


def load_configurations(this_file_dir):
    join = os.path.join(this_file_dir, "../configurations.json")
    configs = open(join, "r")
    r = configs.read()
    return json.loads(r)

CONFIGURATIONS = load_configurations(this_file_dir)



PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_folder = os.path.join(this_file_dir, '../data')
AVAILABLE_CORES = multiprocessing.cpu_count()
MAX_CORES = AVAILABLE_CORES - 2  # the parallelization will use at most (AVAILABLE_CORES - CORES_UNUSED) cores


SRID = 3857

FA2_OPTIONS = {'max_iter': 500,
               'strong_gravity_mode': True,
               'barnes_hut_theta': 1.2,
               'outbound_attraction_distribution': False,
               'gravity': 1,
               'scaling_ratio': 1}

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
