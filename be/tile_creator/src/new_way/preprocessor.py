import pandas as pd

from be.configuration import CONFIGURATIONS


class DataPreprocessor:

    def __init__(self):
        self.FAKE_AMOUNT = 1.0
        self.FAKE_BLOCK_NUMBER = 1

    def preprocess(self, data):
        self._check_fake_vertices_are_unused(data)
        result = self._remove_parallel_edges(data)
        result = self._add_fake_vertices(result)
        return result

    def _check_fake_vertices_are_unused(self, data):
        if CONFIGURATIONS['fake_vertex_1'] in data['target'].values or \
                CONFIGURATIONS['fake_vertex_1'] in data['source'].values or \
                CONFIGURATIONS['fake_vertex_2'] in data['target'].values or \
                CONFIGURATIONS['fake_vertex_2'] in data['source'].values:
            raise Exception(
                "Fake addresses are in use, either chanhe the fake addresses in configuration or rename them in the data")

    def _remove_parallel_edges(self, data):
        data['amount'] = pd.to_numeric(data['amount'])
        data = data.groupby(['source', 'target'], as_index=False).sum()
        return data

    def _add_fake_vertices(self, data):
        """
        We add two fake nodes that will be later positioned such that the resulting layout is a square
        """
        block_number = {'blockNumber': CONFIGURATIONS['fake_vertex_block_number']} \
            if 'block_number' in data.columns or 'blockNumber' in data.columns \
            else {}

        shared = {'amount': CONFIGURATIONS['fake_vertex_amount'],
                  **block_number}

        data = data.append([{'source': CONFIGURATIONS['fake_vertex_1'],
                             'target': CONFIGURATIONS['fake_vertex_1'],
                             **shared}], ignore_index=True)

        data = data.append([{'source': CONFIGURATIONS['fake_vertex_2'],
                             'target': CONFIGURATIONS['fake_vertex_2'],
                             **shared}], ignore_index=True)
        return data
