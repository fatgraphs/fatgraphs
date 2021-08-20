import cudf
import cugraph
import pandas as pd

from be.tile_creator.src.preprocessor import DataPreprocessor


class TokenGraph:

    def __init__(self, path, options):
        """
        :param path: path of the csv file
        :param options: dictionary of args to pass to the pandas read_csv fiunction

        """
        self.raw_data = self.getData(options, path)
        self.preprocessor = DataPreprocessor()
        self.preprocessed_data = self.preprocess()


        self.address_to_id = self.map_addresses_to_ids()
        self.edge_ids_to_amount = self.make_edge_ids_to_amount()
        self.edge_ids_to_amount_cudf = cudf.DataFrame.from_pandas(self.edge_ids_to_amount)
        # self.edge_ids_to_amount_cudf = self.edge_ids_to_amount_cudf.rename(
        #     columns={'vertex_x': 'vertexX', 'vertexY': 'vertexY'})

        self.gpuFrame = self.makeGraphGpuFrame()
        self.degrees = self.get_vertex_degrees()

    def get_vertex_degrees(self):
        degrees = self.gpuFrame.degrees().to_pandas() \
            .sort_values(by=['vertex']) \
            .rename(columns={'in_degree': 'inDegree',
                             'out_degree': 'outDegree'})
        return degrees.set_index('vertex')

    def getData(self, options, path):
        rawData = pd.read_csv(path, **options)
        return rawData

    def preprocess(self):
        preprocessed = self.preprocessor.preprocess(self.raw_data)
        return preprocessed

    def map_addresses_to_ids(self):
        unique_addresses = self._extract_unique_addresses()
        # indices to vertices
        mapping = pd.DataFrame(unique_addresses)\
            .reset_index()\
            .rename(columns={"index": "vertex", 0: "address"})
        return mapping


    def makeGraphGpuFrame(self):
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(self.edge_ids_to_amount_cudf, source='sourceId', destination='targetId')
        return graph

    def make_edge_ids_to_amount(self):
        # associate source id with source address
        data = self.preprocessed_data.merge(self.address_to_id.rename(columns={"address": "source"})).rename(
            columns={"vertex": "sourceId"})
        # associate target_id with target address
        data = data.merge(self.address_to_id.rename(columns={"address": "target"})).rename(
            columns={"vertex": "targetId"})
        data = data[["sourceId", "targetId", "amount"]]
        data = data.sort_values(['sourceId', 'targetId'])
        data = data.reset_index(drop=True)
        return data

    def _extract_unique_addresses(self):
        # get unique addresses
        columnValues = self.preprocessed_data[["source", "target"]].values.ravel()
        uniqueValues = pd.unique(columnValues)
        return uniqueValues

