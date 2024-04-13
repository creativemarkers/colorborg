import unittest
from universalMethods import Uni

class uniMethods:
    def __init__(self):
        uni = Uni()

class BaseTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obj = Uni()

class TestDirectionDecider(BaseTestClass):

    def test_OrdinalDirections(self):
        result = self.obj.directionDecider((3109,3433),(3093,3442))
        self.assertEqual(result, "northWest")
        result = self.obj.directionDecider((3093,3442),(3109,3433))
        self.assertEqual(result,"southEast")
        result = self.obj.directionDecider((4000,4000),(4500,3500))
        self.assertEqual(result,"southEast")
        result = self.obj.directionDecider((4000,4000),(3500,3500))
        self.assertEqual(result,"southWest")
        result = self.obj.directionDecider((4000,4000),(4500,4500))
        self.assertEqual(result,"northEast")
        result = self.obj.directionDecider((0,0),(7,10))
        self.assertEqual(result,"northEast")
        
    def test_CardinalDirections(self):
        result = self.obj.directionDecider((3109,3433),(3109,3442))
        self.assertEqual(result,"north")
        result = self.obj.directionDecider((3109,3500),(3109,3000))
        self.assertEqual(result,"south")
        result = self.obj.directionDecider((3109,3000),(3400,3000))
        self.assertEqual(result,"east")
        result = self.obj.directionDecider((4000,3433),(3000,3442))
        self.assertEqual(result,"west")

    def test_EdgeCases(self):
        with self.assertRaises(ValueError):
            self.obj.directionDecider((0,0),(0,0))
        with self.assertRaises(ValueError):
            self.obj.directionDecider("north","south")
        with self.assertRaises(TypeError):
            self.obj.directionDecider("NW","SE")
        with self.assertRaises(TypeError):
            self.obj.directionDecider((0,0),(0,1),(0,2))
        with self.assertRaises(ValueError):
            self.obj.directionDecider(None,None)

class TestClickAreaDecider(BaseTestClass):

    def test_ExpectedCases(self):
        result = self.obj.clickAreaDecider("northEast","west")
        self.assertEqual(result,(848,155))
        result = self.obj.clickAreaDecider("north","north")
        self.assertEqual(result,(810,54))
        result = self.obj.clickAreaDecider("south","north")
        self.assertEqual(result,(810,176))
        result = self.obj.clickAreaDecider("north","south")
        self.assertEqual(result,(810,176))
        result = self.obj.clickAreaDecider("east","south")
        self.assertEqual(result,(748,114))
        result = self.obj.clickAreaDecider("southWest","east")
        self.assertEqual(result,(848,155))
        result = self.obj.clickAreaDecider("northEast","southWest")
        self.assertEqual(result,(810,176))
        result = self.obj.clickAreaDecider("northWest","west")
        self.assertEqual(result,(852,71))
        result = self.obj.clickAreaDecider("northEast","northWest")
        self.assertEqual(result,(871,114))
        result = self.obj.clickAreaDecider("northEast","southWest")
        self.assertEqual(result,(810,176))


# class TestGetCameraFacingDirection(unittest.TestCase):
#     pass


if __name__ == "__main__":
    unittest.main()