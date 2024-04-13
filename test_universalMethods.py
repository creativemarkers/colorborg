import unittest
from universalMethods import Uni

class TestDirectionDecider(unittest.TestCase):

    uni = Uni()

    def test_OrdinalDirections(self):
        result = self.uni.directionDecider((3109,3433),(3093,3442))
        self.assertEqual(result, "northWest")
        result = self.uni.directionDecider((3093,3442),(3109,3433))
        self.assertEqual(result,"southEast")
        result = self.uni.directionDecider((4000,4000),(4500,3500))
        self.assertEqual(result,"southEast")
        result = self.uni.directionDecider((4000,4000),(3500,3500))
        self.assertEqual(result,"southWest")
        result = self.uni.directionDecider((4000,4000),(4500,4500))
        self.assertEqual(result,"northEast")
        result = self.uni.directionDecider((0,0),(7,10))
        self.assertEqual(result,"northEast")
        
    def test_CardinalDirections(self):
        result = self.uni.directionDecider((3109,3433),(3109,3442))
        self.assertEqual(result,"north")
        result = self.uni.directionDecider((3109,3500),(3109,3000))
        self.assertEqual(result,"south")
        result = self.uni.directionDecider((3109,3000),(3400,3000))
        self.assertEqual(result,"east")
        result = self.uni.directionDecider((4000,3433),(3000,3442))
        self.assertEqual(result,"west")


if __name__ == "__main__":
    unittest.main()