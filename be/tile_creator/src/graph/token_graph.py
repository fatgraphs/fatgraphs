import cudf
import cugraph
import pandas as pd
from be.tile_creator.src.layout.layout_generator import LayoutGenerator
from be.tile_creator.src.preprocessor import DataPreprocessor


class TokenGraph:

    def __init__(self, path, options, labels=None):
        '''

        :param path: path of the csv file
        :param options: dictionary of args to pass to the pandas read_csv fiunction
        :param labels: path of the file that contains labels for the nodes in the graph
            (eg labels indicating exchanges)
        '''
        raw = pd.read_csv(path, **options)
        preprocessor = DataPreprocessor()
        preprocessed = preprocessor.preprocess(raw)
        self.raw_data = preprocessed
        self.addresses_to_ids = self._map_addresses_to_ids()
        self._make_layout()
        self.vertices_metadata = pd.DataFrame(columns=['address', 'label', 'x', 'y'])
        if labels is not None:
            raw_labels = pd.read_csv(labels)
            address_to_label = raw_labels[['address', 'label']]
            self.vertices_metadata = address_to_label.merge(self.addresses_to_positions, on="address")
            self.vertices_metadata = self.vertices_metadata.drop_duplicates()
        temp_max_x = self.ids_to_positions['x'].max()
        temp_max_y = self.ids_to_positions['y'].max()
        temp_min_x = self.ids_to_positions['x'].min()
        temp_min_y = self.ids_to_positions['y'].min()
        min_coordinate_value = min(temp_min_x, temp_min_y)
        max_coordinate_value = max(temp_max_x, temp_max_y)
        # save min and max coordinate value for later using it to place markers on the map
        # (needed to convert from graph coordinate space to map coordinate space)
        self.graph_metadata = pd.DataFrame(data={'min': [min_coordinate_value],
                                                 'max': [max_coordinate_value],
                                                 'nodes': [self.addresses_to_ids.shape[0]],
                                                 'edges': [self.edge_ids_amounts.shape[0]],
                                                 'median_distance': self.median_distance})

    def _make_layout(self):
        self.gpu_frame = self._make_graph_gpu_frame(self.addresses_to_ids)
        lg = LayoutGenerator()
        self.ids_to_positions = lg.make_layout(self.gpu_frame)
        self.median_distance = lg.median_distance

        self.addresses_to_positions = \
            self.addresses_to_ids.merge(self.ids_to_positions, how='left', on='vertex').drop(columns=['vertex'])

    def _map_addresses_to_ids(self):
        data = self.raw_data
        # get unique addresses
        column_values = data[["source", "target"]].values.ravel()
        unique_values = pd.unique(column_values)
        # indices to vertices
        mapping = pd.DataFrame(unique_values).reset_index().rename(columns={"index": "vertex", 0: "address"})
        return mapping

    def _make_graph_gpu_frame(self, addresses_to_ids):
        data = self.raw_data

        # associate source id to the source address
        data = data.merge(addresses_to_ids.rename(columns={"address": "source"})).rename(
            columns={"vertex": "source_id"})

        # associate target_id with target address
        data = data.merge(addresses_to_ids.rename(columns={"address": "target"})).rename(
            columns={"vertex": "target_id"})

        self.edge_ids_amounts = data[["source_id", "target_id", "amount"]]

        data_ids = data[["source_id", "target_id"]]

        data_ids = cudf.DataFrame.from_pandas(data_ids)
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(data_ids, source='source_id', destination='target_id')
        return graph
