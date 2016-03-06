import unittest
from helpers import *


class HelpersTestCase(unittest.TestCase):

    def test_mergeArea(self):
        self.assertTrue(merge_area((1, 2, 3, 4), []) == ((1, 2, 3, 4), []))
        self.assertTrue(merge_area((1, 2, 3, 4), [(0, 1, 5, 6)]) == ((0, 1, 5, 6), []))
        self.assertTrue(merge_area((0, 1, 5, 6), [(1, 2, 3, 4)]) == ((0, 1, 5, 6), []))
        self.assertTrue(merge_area((1, 2, 3, 4), [(0, 1, 3, 4)]) == ((0, 1, 4, 5), []))
        self.assertTrue(merge_area((1, 2, 3, 4), [(10, 11, 3, 4)]) == ((1, 2, 3, 4), [(10, 11, 3, 4)]))
        return

    def test_mergeAreas(self):
        self.assertTrue(merge_areas([], []) == [])
        self.assertTrue(merge_areas([], [(1, 2, 3, 4)]) == [(1, 2, 3, 4)])
        self.assertTrue(merge_areas([], [(1, 2, 3, 4), (0, 1, 5, 6)]) == [(0, 1, 5, 6)])
        self.assertTrue(merge_areas([], [(1, 2, 3, 4), (10, 11, 3, 4)]) == [(1, 2, 3, 4), (10, 11, 3, 4)])
        return

    def test_overlappingAreas(self):
        self.assertTrue(overlapping_areas([], []) == [])
        self.assertTrue(overlapping_areas([], [(1, 2, 3, 4)]) == [])
        self.assertTrue(overlapping_areas([(1, 2, 3, 4)], []) == [(1, 2, 3, 4)])
        self.assertTrue(overlapping_areas([(0, 1, 5, 6)], [(1, 2, 3, 4)]) == [(0, 1, 5, 6)])
        self.assertTrue(overlapping_areas([(1, 2, 3, 4)], [(0, 1, 5, 6)]) == [(0, 1, 5, 6)])
        self.assertTrue(overlapping_areas([(1, 2, 3, 4)], [(0, 1, 5, 4)]) == [(1, 2, 3, 4)])
        return

    def test_sortObjectsByIndex(self):
        self.assertTrue(sort_objects_by_index([], []) == [])
        self.assertTrue((sort_objects_by_index([[1, 2, 3, 4]], [1]) == [[1, 2, 3, 4]]).all())
        self.assertTrue((sort_objects_by_index([[1, 2, 3, 4], [5, 6, 7, 8]], [2, 1]) ==
                         [[1, 2, 3, 4], [5, 6, 7, 8]]).all())
        self.assertTrue((sort_objects_by_index([[1, 2, 3, 4], [5, 6, 7, 8]], [1, 2]) ==
                         [[5, 6, 7, 8], [1, 2, 3, 4]]).all())
        return

if __name__ == '__main__':
    unittest.main()
