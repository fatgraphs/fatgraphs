import math
import unittest
import numpy as np

import gtm
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.test.constants import TEST_DATA_DIR, TEST_DIR, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES, \
    MEDIAN_VERTEX_DISTANCE
from be.utils import calculate_diagonal_square_of_side, find_index_of_nearest
from gtm import get_final_configurations


class TestTransparencyCalculator(unittest.TestCase):
    TOLLERANCE = 0.001  # how many decimals to check for equality of floats

    transparency_calculators = []
    graph_sides = [250, 10e4]  # one small, one large
    stds = [0.1, 0.5, 0.7]
    max_zooms = [2,4,6]

    @classmethod
    def setUpClass(cls):
        for graph_side in cls.graph_sides:
            for std in cls.stds:
                for zoom in cls.max_zooms:
                    config = get_final_configurations({'--csv': TEST_DATA_DIR, "--std": std, '-z': zoom},
                                                      TEST_DIR,
                                                      "test_graph")
                    cls.transparency_calculators.append(TransparencyCalculator(graph_side, config))

    def test_initialisation(cls):
        for tc in cls.transparency_calculators:
            cls.assertIsNotNone(tc)

    def test_throws_exception_if_longest_possible_edge_is_exceeded(cls):
        for tc in cls.transparency_calculators:
            illegal_edge = tc.graph_side * 2
            with cls.assertRaises(Exception):
                tc.calculate_edge_transparencies([illegal_edge])

    def test_all_calculators_can_calculate(cls):
        for tc in cls.transparency_calculators:
            tc.calculate_edge_transparencies([1, 2, 3])

    def test_there_are_as_many_transparency_arrays_as_zoom_levels(cls):
        for tc in cls.transparency_calculators:
            transparencies = tc.calculate_edge_transparencies([1, 2, 3])
            cls.assertEqual(len(transparencies.keys()), tc.zoom_levels)

    def test_longest_edge_has_max_transparency_at_zoom_0(cls):
        for tc in cls.transparency_calculators:
            longest_theoretical_edge = calculate_diagonal_square_of_side(tc.graph_side)
            cls.assertAlmostEqual(tc.calculate_edge_transparencies([longest_theoretical_edge])[0][0], tc.max_t)

    def test_longest_edge_has_min_transparency_at_zoom_6_and_5(cls):
        """
        When completely zoomed in, the longest possible edge should be invisible
        :return:
        """
        for tc in cls.transparency_calculators:
            if tc.zoom_levels == 6:
                longest_theoretical_edge = calculate_diagonal_square_of_side(tc.graph_side)
                cls.assertAlmostEqual(tc.calculate_edge_transparencies([longest_theoretical_edge])[4][0], tc.min_t)
                cls.assertAlmostEqual(tc.calculate_edge_transparencies([longest_theoretical_edge])[5][0], tc.min_t)

    def test_short_edges_have_low_transparency_at_zoom_0(cls):
        for tc in cls.transparency_calculators:
            short_edge = 1 / tc.graph_side
            # the higher the std the more visible short edges will be
            # therefore we need to be more tollerant
            additional_tollerance = (tc.std - 0.1) / 17
            transparency_of_short_edge = tc.calculate_edge_transparencies([short_edge])[0][0]
            cls.assertAlmostEqual(transparency_of_short_edge, tc.min_t, delta=cls.TOLLERANCE + additional_tollerance)

    def test_transparency_gaussian_is_centered_at_edges_that_are_2_tiles_long(cls):
        for tc in cls.transparency_calculators:
            longest_theoretical_edge = calculate_diagonal_square_of_side(tc.graph_side)
            edges = np.arange(1, longest_theoretical_edge, 1.5)
            transparencies = tc.calculate_edge_transparencies(edges)
            for zoom in transparencies.keys():
                if zoom == 0:
                    # we don't test for zoom 0
                    continue
                # how many values to consider left & right of the mean
                window_size = int(max(0, (tc.std - 0.2) * 10) + 2)
                mean = longest_theoretical_edge * (2 / (2 ** zoom))
                index_mean = find_index_of_nearest(edges, mean)
                peak_of_gaussian = transparencies[zoom][index_mean - window_size + 1: index_mean + window_size]
                for transparency in peak_of_gaussian:
                    cls.assertAlmostEqual(transparency, tc.max_t, delta=tc.max_t * 0.1)

    def test_(cls):
        pass

    def test_(cls):
        pass


