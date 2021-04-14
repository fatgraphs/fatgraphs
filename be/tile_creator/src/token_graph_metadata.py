import pandas as pd
from cuml.neighbors import NearestNeighbors


class TokenGraphMetadata:
    """
    :param labels: path of the file that contains labels for the nodes in the graph
            (eg labels indicating exchanges)
    """

    def __init__(self, token_graph, configuration_dictionary, labels=None):
        self.vertices_metadata = pd.DataFrame(columns=['address', 'label', 'x', 'y'])
        if labels is not None:
            raw_labels = pd.read_csv(labels)
            address_to_label = raw_labels[['address', 'label']]
            self.vertices_metadata = address_to_label.merge(token_graph.id_address_pos, on="address")
            self.vertices_metadata = self.vertices_metadata.drop_duplicates()

        max_coordinate_value, min_coordinate_value = self._get_min_max_coordinates(token_graph)

        # save min and max coordinate value for later using it to place markers on the map
        # (needed to convert from graph coordinate space to map coordinate space)
        configuration_frame = pd.DataFrame(data=configuration_dictionary, index=[0])
        graph_dependent_metadata = pd.DataFrame(data={'min': [min_coordinate_value],
                                                      'max': [max_coordinate_value],
                                                      'vertices': [token_graph.id_address_pos.shape[0]],
                                                      'edges': [token_graph.edge_amounts.shape[0]]})
        self.graph_metadata = pd.concat([configuration_frame, graph_dependent_metadata], axis=1)
        # TODO refactor this is messyy
        distance = self.compute_median_distance(token_graph, configuration_dictionary, min_coordinate_value,
                                                max_coordinate_value)
        self.graph_metadata['median_pixel_distance'] = distance

    def _get_min_max_coordinates(self, token_graph):
        temp_max_x = token_graph.id_address_pos['x'].max()
        temp_max_y = token_graph.id_address_pos['y'].max()
        temp_min_x = token_graph.id_address_pos['x'].min()
        temp_min_y = token_graph.id_address_pos['y'].min()
        min_coordinate_value = min(temp_min_x, temp_min_y)
        max_coordinate_value = max(temp_max_x, temp_max_y)
        return max_coordinate_value, min_coordinate_value

    def compute_median_distance(self, token_graph, configuration_dictionary, min_coordinate_value,
                                max_coordinate_value):
        convertt = self.get_converter(configuration_dictionary, min_coordinate_value, max_coordinate_value)

        def tuple_to_columns(row):
            t = convertt((row['x'], row['y']))
            return pd.Series(data=[t[0], t[1]])

        model = NearestNeighbors(n_neighbors=3)
        layout = token_graph.id_address_pos[['x', 'y']]

        layout = layout.apply(tuple_to_columns, axis=1).rename(columns={0: 'x', 1: 'y'})

        model.fit(layout[["x", "y"]].to_numpy())
        distances, indices = model.kneighbors(layout[["x", "y"]])
        median = pd.DataFrame(distances).iloc[:, 1].median()
        return median

    def get_converter(self, configuration_dictionary, min_coordinate, max_coordinate):
        def convert_graph_coordinate_to_map(graph_coordinate):
            graph_side = max_coordinate - min_coordinate
            map_x = (graph_coordinate[0] + abs(max_coordinate)) * configuration_dictionary['tile_size'] / graph_side
            map_y = (graph_coordinate[1] + abs(min_coordinate)) * configuration_dictionary['tile_size'] / graph_side
            return (- map_y / 2, map_x / 2)

        return convert_graph_coordinate_to_map
