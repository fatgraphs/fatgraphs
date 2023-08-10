import cudf

from be.tile_creator_2.preprocessor import DataPreprocessor
from be.utils import timeit


def _load_csv(path):
    rawData = cudf.read_csv(path)
    try:
        rawData['amount'] = rawData['amount'].astype({'amount': 'float64'})
    except Exception as e:
        raise Exception("The column \'amount\' needs to be present in the raw data.")

    if "edgeType" not in rawData.columns:
        # if not type specified, all rows are same type
        rawData['edgeType'] = 1

    return rawData


class DataSource:

    @timeit("Loading the raw file")
    def __init__(self, path):
        raw_data = _load_csv(path)
        preprocessor = DataPreprocessor()
        self.data = preprocessor.preprocess(raw_data)

    def get_data(self):
        ''' return cudf frame '''
        return self.data
