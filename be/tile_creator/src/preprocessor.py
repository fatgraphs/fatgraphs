import pandas as pd


class DataPreprocessor:

    def __init__(self):
        self.FAKE_ADDRESS1 = "0x123456789abcdef01"
        self.FAKE_ADDRESS2 = "0x123456789abcdef02"
        self.FAKE_AMOUNT = 1.0
        self.FAKE_BLOCK_NUMBER = 1

    def preprocess(self, data):
        self._check_fake_addresses_are_unused(data)
        data = self._remove_parallel_edges(data)
        return self._add_two_nodes(data)

    def _remove_parallel_edges(self, data_frame):
        data_frame['amount'] = pd.to_numeric(data_frame['amount'])
        data_frame = data_frame.groupby(['source', 'target'], as_index=False).sum()
        return data_frame

    def _add_two_nodes(self, data):
        data = data.append([{'source': self.FAKE_ADDRESS1, 'target': self.FAKE_ADDRESS2, 'amount': self.FAKE_AMOUNT,
                             'blockNumber': self.FAKE_BLOCK_NUMBER}])
        data = data.append([{'source': self.FAKE_ADDRESS2, 'target': self.FAKE_ADDRESS1, 'amount': self.FAKE_AMOUNT,
                             'blockNumber': self.FAKE_BLOCK_NUMBER}])
        return data

    def _check_fake_addresses_are_unused(self,  data):
        if self.FAKE_ADDRESS1 in data['target'].values or \
                self.FAKE_ADDRESS1 in data['source'].values or \
                self.FAKE_ADDRESS2 in data['target'].values or \
                self.FAKE_ADDRESS2 in data['source'].values:
            raise Exception("Fake addresses are in use")