import pandas as pd


class DataPreprocessor:

    def __init__(self):
        pass

    def preprocess(self, data_frame):
        return self._remove_parallel_edges(data_frame)

    def _remove_parallel_edges(self, data_frame):
        data_frame['amount'] = pd.to_numeric(data_frame['amount'])
        data_frame = data_frame.groupby(['source', 'target'], as_index=False).sum()
        return data_frame