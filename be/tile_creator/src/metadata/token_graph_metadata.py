import pandas as pd
from cuml.neighbors import NearestNeighbors


class TokenGraphMetadata:
    """
    :param labels: path of the file that contains labels for the nodes in the graph
            (eg labels indicating exchanges)
    """

    def __init__(self, token_graph, layout, configuration_dictionary, vertices_labels):
        self.vertices_labels = vertices_labels.vertices_labels

        configuration_dictionary['labels'] = "" if configuration_dictionary['labels'] is None else \
            configuration_dictionary['labels']
        configuration_frame = pd.DataFrame(data=configuration_dictionary, index=[0])
        graph_dependent_metadata = pd.DataFrame(data={
            'median_pixel_distance': layout.median_pixel_distance,
            'min': layout.min,
            'max': layout.max,
            'vertices': [token_graph.address_to_id.shape[0]],
            'edges': [token_graph.edge_ids_to_amount.shape[0]]})
        self.graph_metadata = pd.concat([configuration_frame, graph_dependent_metadata], axis=1)