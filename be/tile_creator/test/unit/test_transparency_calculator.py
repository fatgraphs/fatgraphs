import unittest

from be.configuration import CONFIGURATIONS
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


class ThreeZoomLevelsTest(unittest.TestCase):
    delta = 0.01
    max_output = CONFIGURATIONS['max_transparency']
    min_output = CONFIGURATIONS['min_transparency']

    max_len = 100
    min_len = 2

    c = TransparencyCalculator(min_len, max_len)

    def test_edge_with_legth_equal_to_the_mean_corresponding_to_the_zoom_level_has_max_transparency(self):
        for zoom_level in range(0, CONFIGURATIONS['zoom_levels']):
            step = (ThreeZoomLevelsTest.max_len - ThreeZoomLevelsTest.min_len) / (CONFIGURATIONS['zoom_levels'] + 1)
            mean_at_zoom_zero = step * (CONFIGURATIONS['zoom_levels'] - zoom_level)
            transparency = ThreeZoomLevelsTest.c.get_transparency(mean_at_zoom_zero, zoom_level)
            self.assertAlmostEqual(transparency,
                                   ThreeZoomLevelsTest.max_output,
                                   delta=ThreeZoomLevelsTest.delta)

    def test_edge_transparency_is_within_range(self):
        for edge_len in range(ThreeZoomLevelsTest.min_len, ThreeZoomLevelsTest.max_len):
            for zoom in range(0, CONFIGURATIONS['zoom_levels']):
                transparency = ThreeZoomLevelsTest.c.get_transparency(edge_len, zoom)
                self.assertGreaterEqual(transparency, ThreeZoomLevelsTest.min_output)
                self.assertLessEqual(transparency, ThreeZoomLevelsTest.max_output)
