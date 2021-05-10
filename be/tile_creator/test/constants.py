import os

this_file_path = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = os.path.join(this_file_path, "data", "test_graph.csv")
RAW_EDGES = 278
PREPROCESSED_EDGES = 252
UNIQUE_ADDRESSES = 197
