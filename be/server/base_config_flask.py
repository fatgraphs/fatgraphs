CONFIG_NAME = "base"
USE_MOCK_EQUIVALENCY = False
DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_ROOT = "tokengallery"
VERTEX_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_vertex"
EDGE_TABLE_NAME = lambda graph_id: f"graph_{graph_id}_edge"
SECRET_KEY = "You can't see California without Marlon Widgeto's eyes"

