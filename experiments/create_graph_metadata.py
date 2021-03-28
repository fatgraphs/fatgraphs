from be.configuration import MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH
from be.tile_creator.src.graph.token_graph import TokenGraph

# create metadata file tha is served by the server
# this is generated as a one-off experiment for testing, in the future the metadata creation should be included
# in the main pipeline


medium_graph = TokenGraph(MOCK_LABELLED_RAW_PATH, {'dtype': {'amount': object}}, LABELS_PATH)
# TODO organise better (ie move somegwere else)
metadata = medium_graph.nodes_metadata.drop_duplicates()
metadata.to_csv('metadata.csv', index=False)


