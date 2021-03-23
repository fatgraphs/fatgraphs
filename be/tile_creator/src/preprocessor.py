import cudf
import cugraph
import pandas as pd


class DataPreprocessor:

    def __init__(self):
        pass

    def preprocess(self, data_frame):
        # data_frame.loc[data_frame['source'] == data_frame['target']]
        return data_frame
        # TODO remove parallel edges