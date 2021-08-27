import math
import unittest
import numpy as np
import pandas as pd
from be.tile_creator.src.new_way.test.fixtures import TEST_DATA

from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.utils.utils import calculateDiagonalSquareOfSide, findIndexOfNearest
from be.gtm import getFinalConfigurations


class TestTransparencyCalculator(unittest.TestCase):
    TOLLERANCE = 0.001  # how many decimals to check for equality of floats
    ZOOM_0 = 0

    transparencyCalculators = []
    graphSides = [250, 10e4]  # one small, one large
    stds = [0.1, 0.5, 0.7]
    maxZooms = [2, 4, 6]

    @classmethod
    def setUpClass(cls):
        for graphSide in cls.graphSides:
            for std in cls.stds:
                for zoom in cls.maxZooms:
                    config = getFinalConfigurations({'--csv': TEST_DATA,
                                                     "--std": std,
                                                     '-z': zoom,
                                                     '--meanT': 2.0},
                                                    "test_graph")
                    cls.transparencyCalculators.append(TransparencyCalculator(graphSide, config))

    def test_initialisation(cls):
        for tc in cls.transparencyCalculators:
            cls.assertIsNotNone(tc)

    def test_throws_exception_if_there_is_an_edge_longer_than_the_diagonal(cls):
        for tc in cls.transparencyCalculators:
            illegalEdge = tc.graphSide * 2
            with cls.assertRaises(Exception):
                tc.calculateEdgeTransparencies([illegalEdge])

    def test_all_calculators_can_calculate(cls):
        for tc in cls.transparencyCalculators:
            tc.calculateEdgeTransparencies([1, 2, 3])

    def test_there_are_as_many_transparency_arrays_as_zoom_levels(cls):
        for tc in cls.transparencyCalculators:
            transparencies = tc.calculateEdgeTransparencies([1, 2, 3])
            cls.assertEqual(len(transparencies.keys()), tc.zoomLevels)

    def test_longest_edge_has_highest_transparency_at_zoom_0(cls):

        for tc in cls.transparencyCalculators:
            edgesOfAllPossibleLengths = list(
                range(1, math.ceil(calculateDiagonalSquareOfSide(tc.graphSide))))
            edgeTransparencies = tc.calculateEdgeTransparencies(edgesOfAllPossibleLengths)

            transparencyOfLongestEdge = edgeTransparencies[cls.ZOOM_0][len(edgesOfAllPossibleLengths) - 1]
            maxTransparency = max(edgeTransparencies[cls.ZOOM_0])
            cls.assertAlmostEqual(transparencyOfLongestEdge,
                                  maxTransparency)

    def test_longest_edge_has_decreasing_transparencies_across_zoom_levels(cls):
        # TODO generalise better, check that at max zoom the longest edge has min transparency wrt other zoom_levls
        """
        When completely zoomed in, the longest possible edge should be invisible
        :return:
        """
        for tc in cls.transparencyCalculators:
            edgesOfAllPossibleLengths = list(
                range(1, math.ceil(calculateDiagonalSquareOfSide(tc.graphSide))))
            edgeTransparencies = tc.calculateEdgeTransparencies(edgesOfAllPossibleLengths)

            transparenciesLongestEdgeAcrossZooms = []
            for z in range(0, tc.zoomLevels):
                transparenciesLongestEdgeAcrossZooms.append(
                    edgeTransparencies[z][len(edgesOfAllPossibleLengths) - 1])

        cls.assertTrue(pd.Series(transparenciesLongestEdgeAcrossZooms).is_monotonic_decreasing)

    def test_short_edges_have_low_transparency_at_zoom_0(cls):
        # TODO frame as previous one
        # shortes edge has the lowest transparency wrt to othher zoom levels at zoom 0
        # then remove magin number
        for tc in cls.transparencyCalculators:
            shortEdge = 1 / tc.graphSide
            # the higher the std the more visible short edges will be at zoom 0
            # therefore we need to be more tollerant
            additionalTollerance = (tc.std - 0.1) / 17
            transparencyOfShortEdge = tc.calculateEdgeTransparencies([shortEdge])[0][0]
            cls.assertAlmostEqual(transparencyOfShortEdge, tc.minT, delta=cls.TOLLERANCE + additionalTollerance)

    def test_transparency_gaussian_is_centered_at_edges_that_are_2_tiles_long(cls):
        # TODO parametrise the test wrt given configuration (for mean based on tile size)
        for tc in cls.transparencyCalculators:
            longestTheoreticalEdge = calculateDiagonalSquareOfSide(tc.graphSide)
            edges = np.arange(1, longestTheoreticalEdge, 1.5)
            transparencies = tc.calculateEdgeTransparencies(edges)
            for zoom in transparencies.keys():
                if zoom == 0:
                    # we don't test for zoom 0
                    continue
                # how many values to consider left & right of the mean
                windowSize = int(max(1, (0.3 - tc.std) * 10))
                mean = tc.graphSide * (2 / (2 ** zoom))
                indexMean = findIndexOfNearest(edges, mean)
                peakOfGaussian = transparencies[zoom][indexMean - windowSize + 1: indexMean + windowSize]
                for transparency in peakOfGaussian:
                    cls.assertAlmostEqual(transparency,
                                          max(transparencies[zoom]),
                                          delta=tc.maxT * 0.3,
                                          msg="Failed at zoom {0}".format(zoom))
