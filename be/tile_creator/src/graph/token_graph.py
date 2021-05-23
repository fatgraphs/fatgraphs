import cudf
import cugraph
import pandas as pd
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.preprocessor import DataPreprocessor


class TokenGraph:

    def __init__(self, path, options):
        """
        :param path: path of the csv file
        :param options: dictionary of args to pass to the pandas read_csv fiunction

        """
        self.raw_data = self._get_data(options, path)
        self.preprocessed_data = self._preprocess()
        self.address_to_id = self._map_addresses_to_ids()
        self.edge_ids_to_amount = self._make_edge_ids_to_amount()
        self.edge_ids_to_amount_cudf = cudf.DataFrame.from_pandas(self.edge_ids_to_amount)
        self.gpu_frame = self._make_graph_gpu_frame()
        self.degrees = self.gpu_frame.degrees().to_pandas().sort_values(by=['vertex'])
        self.degrees = self.degrees.set_index('vertex')

    def _get_data(self, options, path):
        raw_data = pd.read_csv(path, **options)
        return raw_data

    def _map_addresses_to_ids(self):
        # get unique addresses
        column_values = self.preprocessed_data[["source", "target"]].values.ravel()
        unique_values = pd.unique(column_values)
        # indices to vertices
        mapping = pd.DataFrame(unique_values).reset_index().rename(columns={"index": "vertex", 0: "address"})
        return mapping

    def _make_graph_gpu_frame(self):
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(self.edge_ids_to_amount_cudf, source='source_id', destination='target_id')
        return graph

    def _make_edge_ids_to_amount(self):
        # associate source id to the source address
        data = self.preprocessed_data.merge(self.address_to_id.rename(columns={"address": "source"})).rename(
            columns={"vertex": "source_id"})
        # associate target_id with target address
        data = data.merge(self.address_to_id.rename(columns={"address": "target"})).rename(
            columns={"vertex": "target_id"})
        data = data[["source_id", "target_id", "amount"]]
        data = data.sort_values(['source_id', 'target_id'])
        data = data.reset_index(drop=True)
        return data

    def _preprocess(self):
        self.preprocessor = DataPreprocessor()
        preprocessed = self.preprocessor.preprocess(self.raw_data)
        return preprocessed
