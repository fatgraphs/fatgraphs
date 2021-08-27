import pandas as pd

from be.tile_creator.src.new_way.preprocessor import DataPreprocessor


def _load_csv(path, options=None):
    if options is None:
        options = {'dtype': {'amount': float}}
    rawData = pd.read_csv(path, **options)
    return rawData


class DataSource:

    def __init__(self, path, options=None):
        raw_data = _load_csv(path, options)
        preprocessor = DataPreprocessor()
        self.data = preprocessor.preprocess(raw_data)

    def get_data(self):
        return self.data
