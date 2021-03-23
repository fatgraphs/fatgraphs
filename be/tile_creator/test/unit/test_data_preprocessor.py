from be.tile_creator.src.preprocessor import DataPreprocessor
from be.tile_creator.test.unit.generic_graph_test import GenericGraphTest


class DataPreprocessorTest(GenericGraphTest):

    def setUp(self):
        self.preprocessor = DataPreprocessor()

    def test_preprocessor_instanciation(self):
        self.assertIsNotNone(self.preprocessor)

    def test_preprocess(self):
        self.preprocessor.preprocess(self.graphs[0].raw_data)

