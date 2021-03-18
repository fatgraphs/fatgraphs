import os
dir_path = os.path.dirname(os.path.realpath(__file__))
TILE_SOURCE = os.path.join(dir_path, 'tiles')
data_folder = os.path.join(dir_path, 'data')
MEDIUM_GRAPH_RAW_PATH = os.path.join(data_folder, 'medium.csv')