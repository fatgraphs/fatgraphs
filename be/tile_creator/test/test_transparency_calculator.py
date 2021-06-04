import math
import unittest
import numpy as np
import pandas as pd

from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.test.constants import TEST_DATA, TEST_DIR
from be.utils.utils import calculate_diagonal_square_of_side, find_index_of_nearest
from gtm import get_final_configurations


class TestTransparencyCalculator(unittest.TestCase):
    TOLLERANCE = 0.001  # how many decimals to check for equality of floats
    ZOOM_0 = 0

    transparency_calculators = []
    graph_sides = [250, 10e4]  # one small, one large
    stds = [0.1, 0.5, 0.7]
    max_zooms = [2, 4, 6]

    @classmethod
    def setUpClass(cls):
        for graph_side in cls.graph_sides:
            for std in cls.stds:
                for zoom in cls.max_zooms:
                    config = get_final_configurations({'--csv': TEST_DATA,
                                                       "--std": std,
                                                       '-z': zoom,
                                                       '--mean_t': 2.0},
                                                      TEST_DIR,
                                                      "test_graph")
                    cls.transparency_calculators.append(TransparencyCalculator(graph_side, config))

    def test_initialisation(cls):
        for tc in cls.transparency_calculators:
            cls.assertIsNotNone(tc)

    def test_throws_exception_if_there_is_an_edge_longer_than_the_diagonal(cls):
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

    def test_longest_edge_has_highest_transparency_at_zoom_0(cls):

        for tc in cls.transparency_calculators:
            edges_of_all_possible_lengths = list(
                range(1, math.ceil(calculate_diagonal_square_of_side(tc.graph_side))))
            edge_transparencies = tc.calculate_edge_transparencies(edges_of_all_possible_lengths)

            transparency_of_longest_edge = edge_transparencies[cls.ZOOM_0][len(edges_of_all_possible_lengths) - 1]
            max_transparency = max(edge_transparencies[cls.ZOOM_0])
            cls.assertAlmostEqual(transparency_of_longest_edge,
                                  max_transparency)

    def test_longest_edge_has_decreasing_transparencies_across_zoom_levels(cls):
        # TODO generalise better, check that at max zoom the longest edge has min transparency wrt other zoom_levls
        """
        When completely zoomed in, the longest possible edge should be invisible
        :return:
        """
        for tc in cls.transparency_calculators:
            edges_of_all_possible_lengths = list(
                range(1, math.ceil(calculate_diagonal_square_of_side(tc.graph_side))))
            edge_transparencies = tc.calculate_edge_transparencies(edges_of_all_possible_lengths)

            transparencies_longest_edge_across_zooms = []
            for z in range(0, tc.zoom_levels):
                transparencies_longest_edge_across_zooms.append(
                    edge_transparencies[z][len(edges_of_all_possible_lengths) - 1])

        cls.assertTrue(pd.Series(transparencies_longest_edge_across_zooms).is_monotonic_decreasing)

    def test_short_edges_have_low_transparency_at_zoom_0(cls):
        # TODO frame as previous one
        # shortes edge has the lowest transparency wrt to othher zoom levels at zoom 0
        # then remove magin number
        for tc in cls.transparency_calculators:
            short_edge = 1 / tc.graph_side
            # the higher the std the more visible short edges will be at zoom 0
            # therefore we need to be more tollerant
            additional_tollerance = (tc.std - 0.1) / 17
            transparency_of_short_edge = tc.calculate_edge_transparencies([short_edge])[0][0]
            cls.assertAlmostEqual(transparency_of_short_edge, tc.min_t, delta=cls.TOLLERANCE + additional_tollerance)

    def test_transparency_gaussian_is_centered_at_edges_that_are_2_tiles_long(cls):
        # TODO parametrise the test wrt given configuration (for mean based on tile size)
        for tc in cls.transparency_calculators:
            longest_theoretical_edge = calculate_diagonal_square_of_side(tc.graph_side)
            edges = np.arange(1, longest_theoretical_edge, 1.5)
            transparencies = tc.calculate_edge_transparencies(edges)
            for zoom in transparencies.keys():
                if zoom == 0:
                    # we don't test for zoom 0
                    continue
                # how many values to consider left & right of the mean
                window_size = int(max(1, (0.3 - tc.std) * 10))
                mean = tc.graph_side * (2 / (2 ** zoom))
                index_mean = find_index_of_nearest(edges, mean)
                peak_of_gaussian = transparencies[zoom][index_mean - window_size + 1: index_mean + window_size]
                for transparency in peak_of_gaussian:
                    cls.assertAlmostEqual(transparency,
                        max(transparencies[zoom]),
                        delta=tc.max_t * 0.3,
                        msg="Failed at zoom {0}".format(zoom))
