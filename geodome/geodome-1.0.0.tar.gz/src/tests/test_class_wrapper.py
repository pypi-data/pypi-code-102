from geodome.geodesic_dome import GeodesicDome

import numpy as np

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestDomeCreation(unittest.TestCase):
    def test_empty_creation(self):
        gd = GeodesicDome()
        self.assertEqual(len(gd.vertices), 12)
        self.assertEqual(len(gd.triangles), 20)

    def test_freq0_creation(self):
        gd = GeodesicDome(0)
        self.assertEqual(len(gd.vertices), 12)
        self.assertEqual(len(gd.triangles), 20)

    def test_freq1_creation(self):
        gd = GeodesicDome(1)
        self.assertEqual(len(gd.vertices), 42)
        self.assertEqual(len(gd.triangles), 80)

    def test_freq2_creation(self):
        gd = GeodesicDome(2)
        self.assertEqual(len(gd.vertices), 162)
        self.assertEqual(len(gd.triangles), 320)

    def test_getters(self):
        gd = GeodesicDome(2)
        self.assertEqual(len(gd.get_vertices()), 162)
        self.assertEqual(len(gd.get_triangles()), 320)

    def test_tessellation(self):
        gd = GeodesicDome()
        gd.tessellate(2)
        self.assertEqual(len(gd.get_vertices()), 162)
        self.assertEqual(len(gd.get_triangles()), 320)

    def test_neighbourhood(self):
        gd = GeodesicDome()
        neighbours = gd.find_neighbours_vertex(0, 1)
        self.assertEqual(neighbours[0], 0)
        self.assertEqual(neighbours[1], 11)
        self.assertEqual(neighbours[2], 5)
        self.assertEqual(neighbours[3], 1)
        self.assertEqual(neighbours[4], 7)
        self.assertEqual(neighbours[5], 10)

    def test_error_creation(self):
        with self.assertRaises(ValueError):
            gd = GeodesicDome(-1)

    def test_error_tessellate(self):
        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.tessellate(-1)

    def test_error_neighbour(self):
        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.find_neighbours_vertex(1, -1)
        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.find_neighbours_vertex(100, 1)
        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.find_neighbours_vertex(-1, 1)

    def test_error_selective(self):
        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.custom_partial_tessellate_vertex()

        with self.assertRaises(ValueError):
            gd = GeodesicDome()
            gd.custom_partial_tessellate_triangle(np.zeros(0, np.int64))

    def test_selective_neighbourhood(self):
        gd = GeodesicDome()
        neighbours = gd.find_neighbours_vertex(0, 1)
        gd.custom_partial_tessellate_vertex(neighbours)

        self.assertEqual(len(gd.get_vertices()), 37)
        self.assertEqual(len(gd.get_triangles()), 65)

    def test_selective_saved_neighbourhood(self):
        gd = GeodesicDome()
        gd.find_neighbours_vertex(0, 1)
        gd.custom_partial_tessellate_vertex()

        self.assertEqual(len(gd.get_vertices()), 37)
        self.assertEqual(len(gd.get_triangles()), 65)

    # def test_selective
