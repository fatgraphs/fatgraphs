import pandas as pd


class TokenGraphMetadata:

    def __init__(self, token_graph, layout, configuration_dictionary):
        self.configurations = None
        self.graph_data = None

        configuration_dictionary['labels'] = "" if configuration_dictionary['labels'] is None else \
            configuration_dictionary['labels']
        self.configurations = pd.DataFrame(data=configuration_dictionary, index=[0])

        self.graph_data = pd.DataFrame(data={
            'median_pixel_distance': layout.median_pixel_distance,
            'min': layout.min,
            'max': layout.max,
            'vertices': [token_graph.address_to_id.shape[0]],
            'edges': [token_graph.edge_ids_to_amount.shape[0]]})

    def get_graph_name(self):
        return self.configurations['graph_name'][0]

    def get_zoom_levels(self):
        return self.configurations['zoom_levels'][0]

    def get_min_coordinate(self):
        return self.graph_data['min'][0]

    def get_max_coordinate(self):
        return self.graph_data['max'][0]

    def get_single_frame(self):
        return pd.concat([self.configurations, self.graph_data], axis=1)
