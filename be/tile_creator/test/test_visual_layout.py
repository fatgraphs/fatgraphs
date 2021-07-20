import unittest
import numpy as np
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.test.constants import TEST_DATA, TEST_DIR, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES
from gtm import getFinalConfigurations
import math

class TestVisualLayout(unittest.TestCase):

    graph = None
    layout = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        defaultConfig = getFinalConfigurations({'--csv': TEST_DATA},  "test_graph")
        cls.layout = VisualLayout(cls.graph, defaultConfig)

    def test_each_address_has_a_coordinate(cls):
        cls.assertIsNotNone(cls.layout.vertexPositions)
        cls.assertEqual(cls.layout.vertexPositions.shape[0], UNIQUE_ADDRESSES + FAKE_NODES)

    def test_fake_node_are_top_left_and_bottom_right(cls):
        bottomRightVertexPos, topLeftVertexPos = cls.getPositionFakeNodes()
        expectedTopLeftVertexPos = [cls.layout.min] * 2
        expectedBottomRightVertexPos = [cls.layout.max] * 2
        cls.assertListEqual(topLeftVertexPos, expectedTopLeftVertexPos)
        cls.assertListEqual(bottomRightVertexPos, expectedBottomRightVertexPos)

    def test_there_are_other_nodes_that_share_one_of_the_coordinate_of_the_fake_nodes(cls):
        """
        This test ensure that the position of the fake nodes is coherent wrt position of the other 'real nodes'.
        """

        bottomRightVertexPos, topLeftVertexPos = cls.getPositionFakeNodes()
        # the fake nodes are always the last two
        real_nodes = cls.layout.vertexPositions[0:-2]
        singleValuesRealNodes = real_nodes[['x', 'y']].values.flatten()
        cls.assertTrue(bottomRightVertexPos[0] in singleValuesRealNodes and
                       bottomRightVertexPos[1] in singleValuesRealNodes and
                       topLeftVertexPos[0] in singleValuesRealNodes and
                       topLeftVertexPos[1] in singleValuesRealNodes)

    def test_layout_is_square(cls):
        bottomRight = cls.layout.vertexPositions[['x', 'y']].max()
        topLeft = cls.layout.vertexPositions[['x', 'y']].min()
        cls.assertEqual(bottomRight['x'], bottomRight['y'])
        cls.assertEqual(topLeft['x'], topLeft['y'])

    def test_edge_ids_to_positions_are_as_many_as_the_edges(cls):
        cls.assertEqual(cls.layout.edgeIdsToPositions.shape[0], PREPROCESSED_EDGES + FAKE_NODES)

    def test_pixel_coordinates_are_within_tile_bounds(cls):
        pixelMax = cls.layout.edgeIdsToPositionsPixel.max()
        pixelMin = cls.layout.edgeIdsToPositionsPixel.min()
        cls.assertTrue(pixelMax['sourceXPixel'] == pixelMax['sourceYPixel'] == pixelMax['targetXPixel']
                       == pixelMax['targetYPixel'])
        cls.assertTrue(pixelMin['sourceXPixel'] == pixelMin['sourceYPixel'] == pixelMin['targetXPixel']
                       == pixelMin['targetYPixel'])

    def test_vertex_with_highest_degree_has_largest_size(cls):
        # relying on indices of degrees to correspond to ids
        indexOfLargestVertex = cls.graph.degrees.idxmax()['outDegree']
        largest = cls.layout.vertexSizes[indexOfLargestVertex]
        cls.assertEqual(largest, cls.layout.vertexSizes.max())

    def test_vertex_with_smallest_degree_has_smallest_size(cls):
        # relying on indices of degrees to correspond to ids
        indexOfSmallestVertex = cls.graph.degrees.idxmin()['outDegree']
        smallest = cls.layout.vertexSizes[indexOfSmallestVertex]
        cls.assertEqual(smallest, cls.layout.vertexSizes.min())

    def test_edges_with_largest_amount_is_thickest(cls):
        # because of clipping we can get many values that are the largest thickness
        indexesMaxThickness = list(np.where(cls.layout.edgeThickness == cls.layout.edgeThickness.max())[0])
        indexHighestAmount = cls.graph.edgeIdsToAmount['amount'].idxmax()
        cls.assertIn(indexHighestAmount, indexesMaxThickness)

    def test_edges_with_smallest_amount_is_thinnest(cls):
        # because of clipping we can get many values that are the smallest thickness
        indexesMinThickness = list(np.where(cls.layout.edgeThickness == cls.layout.edgeThickness.min())[0])
        indexMinAmount = cls.graph.edgeIdsToAmount['amount'].idxmin()
        cls.assertIn(indexMinAmount, indexesMinThickness)

    def test_edge_lengths_are_right_order(cls):
        """
        Edge lengths should be in such an order that they match the order of the edge list.
        I.E. element i in the edge_lenghts corresponds to the length of edge i in the edge list.
        :return:
        """
        edgeLengths = cls.layout.edgeLengths
        vertexPositions = cls.layout.vertexPositions
        for index, edge in cls.graph.edgeIdsToAmount.iterrows():
            source = vertexPositions[['x', 'y']].iloc[int(edge.sourceId)]
            target = vertexPositions[['x', 'y']].iloc[int(edge.targetId)]
            source = [source['x'], source['y']]
            target = [target['x'], target['y']]
            expectedEdgeLength = math.dist(source, target)
            actualEdgeLength = edgeLengths[index]
            cls.assertAlmostEqual(expectedEdgeLength, actualEdgeLength, delta=0.001)

    def getPositionFakeNodes(cls):
        maxId = cls.graph.addressToId['vertex'].max()
        maxId2 = maxId - 1
        topLeftVertexPos = list(cls.layout.vertexPositions[maxId:maxId + 1][['x', 'y']].values[0])
        bottomRightVertexPos = list(cls.layout.vertexPositions[maxId2:maxId2 + 1][['x', 'y']].values[0])
        return bottomRightVertexPos, topLeftVertexPos

