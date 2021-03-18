import cudf
import cugraph
import pandas as pd
from be.tile_creator.src.layout.layout_generator import LayoutGenerator


class TokenGraph:

    def __init__(self, path, options):
        self.raw_data = pd.read_csv(path, **options)
        self.addresses_to_ids = self._map_addresses_to_ids()
        self.gpu_frame = self._make_graph_gpu_frame(self.addresses_to_ids)
        lg = LayoutGenerator()
        self.layout = lg.make_layout(self.gpu_frame)

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
