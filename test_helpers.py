import unittest
from helpers import *

class helpersTestCase(unittest.TestCase):
    def test_mergeArea(self):
        self.assertTrue(mergeArea((1,2,3,4),[]) == ((1,2,3,4),[]))
        self.assertTrue(mergeArea((1,2,3,4),[(0,1,5,6)]) == ((0,1,5,6),[]))
        self.assertTrue(mergeArea((0,1,5,6),[(1,2,3,4)]) == ((0,1,5,6),[]))
        self.assertTrue(mergeArea((1,2,3,4),[(0,1,3,4)]) == ((0,1,4,5),[]))
        self.assertTrue(mergeArea((1,2,3,4),[(10,11,3,4)]) == ((1,2,3,4),[(10,11,3,4)]))
        return
    def test_mergeAreas(self):
        self.assertTrue(mergeAreas([],[]) == [])
        self.assertTrue(mergeAreas([],[(1,2,3,4)]) == [(1,2,3,4)])
        self.assertTrue(mergeAreas([],[(1,2,3,4),(0,1,5,6)]) == [(0,1,5,6)])
        self.assertTrue(mergeAreas([],[(1,2,3,4),(10,11,3,4)]) == [(1,2,3,4),(10,11,3,4)])
        return
    def test_overlappingAreas(self):
        self.assertTrue(overlappingAreas([],[]) == [])
        self.assertTrue(overlappingAreas([],[(1,2,3,4)]) == [])
        self.assertTrue(overlappingAreas([(1,2,3,4)],[]) == [(1,2,3,4)])
        self.assertTrue(overlappingAreas([(0,1,5,6)],[(1,2,3,4)]) == [(0,1,5,6)])
        self.assertTrue(overlappingAreas([(1,2,3,4)],[(0,1,5,6)]) == [(0,1,5,6)])
        self.assertTrue(overlappingAreas([(1,2,3,4)],[(0,1,5,4)]) == [(1,2,3,4)])
        return

if __name__ == '__main__':
    unittest.main()

