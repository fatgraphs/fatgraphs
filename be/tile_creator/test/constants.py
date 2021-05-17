import os

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data", "test_graph.csv")
TEST_OUTPUT_DIR = os.path.join(TEST_DIR, "data", "output")
TEST_REFERENCE_OUTPUT_DIR = os.path.join(TEST_DIR, "data", "reference_output")
IMG_SIMILARITY_DIR = os.path.join(TEST_DIR, "data", "img_similarity")
SMALL_SIMILAR_GRAPHS_DIR = os.path.join(IMG_SIMILARITY_DIR, 'small')
MEDIUM_SIMILAR_GRAPHS_DIR = os.path.join(IMG_SIMILARITY_DIR, 'medium')
RAW_EDGES = 278
PREPROCESSED_EDGES = 252
UNIQUE_ADDRESSES = 197
FAKE_NODES = 2
