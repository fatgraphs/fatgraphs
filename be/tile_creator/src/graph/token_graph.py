import cudf
import cugraph
import pandas as pd
from be.tile_creator.src.layout.layout_generator import LayoutGenerator
from be.tile_creator.src.preprocessor import DataPreprocessor


class TokenGraph:

    def __init__(self, path, options):
        """
        :param path: path of the csv file
        :param options: dictionary of args to pass to the pandas read_csv fiunction

        id_address_pos: mapping between a vertex id, it's corresponding eth address and the position determined by the
            layout algorithm
        """
        self.data = self._get_data(options, path)
        addresses_to_ids = self._map_addresses_to_ids()
        self.edge_amounts = self._make_edge_ids_to_amount(addresses_to_ids)
        self.gpu_frame = self._make_graph_gpu_frame()
        self.degree = self.gpu_frame.degrees()
        self.id_address_pos = self._make_layout(addresses_to_ids)

    def _get_data(self, options, path):
        raw_data = pd.read_csv(path, **options)
        preprocessor = DataPreprocessor()
        preprocessed = preprocessor.preprocess(raw_data)
        return preprocessed

    def _make_layout(self, addresses_to_ids):
        lg = LayoutGenerator()
        ids_to_positions = lg.make_layout(self.gpu_frame)
        return addresses_to_ids.merge(ids_to_positions)

    def _map_addresses_to_ids(self):
        # get unique addresses
        column_values = self.data[["source", "target"]].values.ravel()
        unique_values = pd.unique(column_values)
        # indices to vertices
        mapping = pd.DataFrame(unique_values).reset_index().rename(columns={"index": "vertex", 0: "address"})
        return mapping

    def _make_graph_gpu_frame(self):
        data_ids = self.edge_amounts[["source_id", "target_id"]]
        data_ids = cudf.DataFrame.from_pandas(data_ids)
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(data_ids, source='source_id', destination='target_id')
        return graph

    def _make_edge_ids_to_amount(self, addresses_to_ids):
        data = self.data
        # associate source id to the source address
        data = data.merge(addresses_to_ids.rename(columns={"address": "source"})).rename(
            columns={"vertex": "source_id"})
        # associate target_id with target address
        data = data.merge(addresses_to_ids.rename(columns={"address": "target"})).rename(
            columns={"vertex": "target_id"})
        return data[["source_id", "target_id", "amount"]]
