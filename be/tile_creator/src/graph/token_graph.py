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
        self.rawData = self.getData(options, path)
        self.preprocessedData = self.preprocess()
        self.addressToId = self.mapAddressesToIds()
        self.edgeIdsToAmount = self.makeEdgeIdsToAmount()
        self.edgeIdsToAmountCudf = cudf.DataFrame.from_pandas(self.edgeIdsToAmount)
        self.edgeIdsToAmountCudf = self.edgeIdsToAmountCudf.rename(
            columns={'vertex_x': 'vertexX', 'vertexY': 'vertexY'})

        self.gpuFrame = self.makeGraphGpuFrame()
        self.degrees = self.gpuFrame.degrees().to_pandas() \
            .sort_values(by=['vertex']) \
            .rename(columns={'in_degree': 'inDegree',
                             'out_degree': 'outDegree'})
        self.degrees = self.degrees.set_index('vertex')

    def getData(self, options, path):
        rawData = pd.read_csv(path, **options)
        return rawData

    def mapAddressesToIds(self):
        # get unique addresses
        columnValues = self.preprocessedData[["source", "target"]].values.ravel()
        uniqueValues = pd.unique(columnValues)
        # indices to vertices
        mapping = pd.DataFrame(uniqueValues).reset_index().rename(columns={"index": "vertex", 0: "address"})
        return mapping

    def makeGraphGpuFrame(self):
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(self.edgeIdsToAmountCudf, source='sourceId', destination='targetId')
        return graph

    def makeEdgeIdsToAmount(self):
        # associate source id to the source address
        data = self.preprocessedData.merge(self.addressToId.rename(columns={"address": "source"})).rename(
            columns={"vertex": "sourceId"})
        # associate target_id with target address
        data = data.merge(self.addressToId.rename(columns={"address": "target"})).rename(
            columns={"vertex": "targetId"})
        data = data[["sourceId", "targetId", "amount"]]
        data = data.sort_values(['sourceId', 'targetId'])
        data = data.reset_index(drop=True)
        return data

    def preprocess(self):
        self.preprocessor = DataPreprocessor()
        preprocessed = self.preprocessor.preprocess(self.rawData)
        return preprocessed
