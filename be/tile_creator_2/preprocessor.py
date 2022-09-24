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
        if CONFIGURATIONS['corner_vertices']['fake_vertex_1'] in data['target'].to_array() or \
                CONFIGURATIONS['corner_vertices']['fake_vertex_1'] in data['source'].to_array() or \
                CONFIGURATIONS['corner_vertices']['fake_vertex_2'] in data['target'].to_array() or \
                CONFIGURATIONS['corner_vertices']['fake_vertex_2'] in data['source'].to_array():
            raise Exception(
                "Fake addresses are in use, either chanhe the fake addresses in configuration or rename them in the data")

    def _remove_parallel_edges(self, data):
        # if parallel edges are removed we must discard the blockNumber
        if "blockNumber" in data.columns:
            data.drop('blockNumber', axis=1)
        data = data.groupby(['source', 'target', 'edgeType'], as_index=False).sum()
        return data

    def _add_fake_vertices(self, data):
        """
        We add two fake nodes that will be later positioned such that the resulting layout is a square
        """
        block_number = {'blockNumber': CONFIGURATIONS['corner_vertices']['fake_vertex_block_number']} \
            if 'block_number' in data.columns or 'blockNumber' in data.columns \
            else {}

        shared = {'amount': CONFIGURATIONS['corner_vertices']['fake_vertex_amount'],
                  **block_number}

        data = data.append([{'source': CONFIGURATIONS['corner_vertices']['fake_vertex_1'],
                             'target': CONFIGURATIONS['corner_vertices']['fake_vertex_1'],
                             'edgeType': 99,
                             **shared}], ignore_index=True)

        data = data.append([{'source': CONFIGURATIONS['corner_vertices']['fake_vertex_2'],
                             'target': CONFIGURATIONS['corner_vertices']['fake_vertex_2'],
                             'edgeType': 99,
                             **shared}], ignore_index=True)
        return data
