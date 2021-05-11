import unittest
import numpy as np

import gtm
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.test.constants import TEST_DATA, TEST_FOLDER, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES, \
    MEDIAN_VERTEX_DISTANCE
from gtm import get_final_configurations


class TestTransparencyCalculator(unittest.TestCase):
    TOLLERANCE = 0.001  # how many decimals to check for equality of floats

    transparency_calculators = []
    graph_sides = [250, 10e4]  # one small, one large
    stds = [0.1, 0.5, 0.7]

    @classmethod
    def setUpClass(cls):
        for graph_side in cls.graph_sides:
            for std in cls.stds:
                config = get_final_configurations({'--csv': TEST_DATA, "--std": std},
                                                  TEST_FOLDER,
                                                  "test_graph")
                cls.transparency_calculators.append(TransparencyCalculator(graph_side, config))

    def test_initialisation(cls):
        for tc in cls.transparency_calculators:
            cls.assertIsNotNone(tc)

    def test_all_calculators_can_calculate(cls):
        for tc in cls.transparency_calculators:
            tc.calculate_edge_transparencies([1, 2, 3])

    def test_edges_as_long_as_graph_side_have_max_transparency_at_zoom_0(cls):
        for tc in cls.transparency_calculators:
            cls.assertAlmostEqual(tc.calculate_edge_transparencies([tc.graph_side])[0][0], tc.max_t)

    def test_short_edges_have_low_transparency_at_zoom_0(cls):
        for tc in cls.transparency_calculators:
            short_edge = 1 / tc.graph_side
            # the higher the std the more visible short edges will be
            # therefore we need to be more tollerant
            additional_tollerance = (tc.std - 0.1) / 17
            transparency_of_short_edge = tc.calculate_edge_transparencies([short_edge])[0][0]
            cls.assertAlmostEqual(transparency_of_short_edge, tc.min_t, delta=cls.TOLLERANCE + additional_tollerance)

    def test_at_zoom_0_edges_longer_than_graph_side_are_visible(cls):
        pass

    def test_at_zoom_0_edges_shorter_than_graph_side_are_invisible(cls):
        pass
