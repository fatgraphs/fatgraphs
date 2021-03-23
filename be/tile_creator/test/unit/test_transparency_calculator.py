import unittest

from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


class TwoZoomLevelsTest(unittest.TestCase):

    delta = 0.01

    def test_max_length_edges_are_either_invisible_or_fully_opaque(self):
        c = TransparencyCalculator(0, 100, 2)
        self.assertAlmostEqual(c.get_transparency(100, 0), 1, delta=TwoZoomLevelsTest.delta)
        self.assertAlmostEqual(c.get_transparency(100, 1), 0, delta=TwoZoomLevelsTest.delta)
        self.assertAlmostEqual(c.get_transparency(0, 0), 0, delta=TwoZoomLevelsTest.delta)
        self.assertAlmostEqual(c.get_transparency(0, 1), 1, delta=TwoZoomLevelsTest.delta)

    def test_half_max_len_edge_has_0_25_opacity(self):
        c = TransparencyCalculator(0, 100, 2)
        self.assertAlmostEqual(c.get_transparency(50, 0), 0.25, delta=TwoZoomLevelsTest.delta)
        self.assertAlmostEqual(c.get_transparency(50, 1), 0.25, delta=TwoZoomLevelsTest.delta)
        self.assertEqual(c.get_transparency(50, 1), c.get_transparency(50, 0))

class FiveZoomLevels(unittest.TestCase):

    delta = 0.1

    def test_zoom_0(self):
        c = TransparencyCalculator(1, 101, 5)
        self.assertAlmostEqual(c.get_transparency(101, 0), 1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(75, 0), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(50, 0), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(25, 0), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(0, 0), 0, delta=FiveZoomLevels.delta)

    def test_zoom_1(self):
        c = TransparencyCalculator(1, 101, 5)
        self.assertAlmostEqual(c.get_transparency(101, 1), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(75, 1), 1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(50, 1), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(25, 1), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(0, 1), 0, delta=FiveZoomLevels.delta)

    def test_zoom_2(self):
        c = TransparencyCalculator(1, 101, 5)
        self.assertAlmostEqual(c.get_transparency(101, 2), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(75, 2), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(50, 2), 1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(25, 2), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(0, 2), 0, delta=FiveZoomLevels.delta)

    def test_zoom_3(self):
        c = TransparencyCalculator(1, 101, 5)
        self.assertAlmostEqual(c.get_transparency(101, 3), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(75, 3), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(50, 3), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(25, 3), 1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(0, 3), 0.1, delta=FiveZoomLevels.delta)


    def test_zoom_4(self):
        c = TransparencyCalculator(1, 101, 5)
        self.assertAlmostEqual(c.get_transparency(101, 4), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(75, 4), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(50, 4), 0, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(25, 4), 0.1, delta=FiveZoomLevels.delta)
        self.assertAlmostEqual(c.get_transparency(0, 4), 1, delta=FiveZoomLevels.delta)



