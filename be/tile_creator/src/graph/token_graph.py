import cudf
from cugraph import Graph
import pandas as pd
from be.configuration import CONFIGURATIONS, internal_id, external_id

from be.tile_creator.src.new_way.preprocessor import DataPreprocessor


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
            .rename(columns={
                "index": CONFIGURATIONS['vertex_internal_id'],
                0: CONFIGURATIONS['vertex_external_id']})
        return mapping


    def makeGraphGpuFrame(self):
        graph = Graph()
        graph.from_cudf_edgelist(self.edge_ids_to_amount_cudf, source=internal_id("source"), destination=internal_id("target"))
        return graph

    def make_edge_ids_to_amount(self):
        # associate source id with source address
        data = self.preprocessed_data.merge(self.address_to_id.rename(
            columns={
                CONFIGURATIONS['vertex_external_id']: external_id("source"),
                CONFIGURATIONS['vertex_internal_id']: internal_id('source')
            }), left_on='source', right_on=external_id("source"))

        # associate target_id with target address
        data = data.merge(self.address_to_id.rename(
            columns={
                CONFIGURATIONS['vertex_external_id']: external_id("target"),
                CONFIGURATIONS['vertex_internal_id']: internal_id('target')
            }), left_on='target', right_on=external_id("target"))

        data = data[[internal_id('source'), internal_id('target'), "amount"]]
        data = data.sort_values([internal_id('source'), internal_id('target')])
        data = data.reset_index(drop=True)
        return data

    def _extract_unique_addresses(self):
        # get unique addresses
        columnValues = self.preprocessed_data[["source", "target"]].values.ravel()
        uniqueValues = pd.unique(columnValues)
        return uniqueValues

