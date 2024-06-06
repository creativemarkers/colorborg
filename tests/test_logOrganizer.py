
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
import unittest
from unittest.mock import Mock, patch

try:
    from utils.logOrganizer import LogOrganizer
except ImportError:
    from logOrganizer import LogOrganizer



"""
Normal Cases
Corner Cases
Edge Cases
Negative Cases

Performance Cases

res = result
"""

class BaseTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logOrganizer = LogOrganizer("fisher")

class TestisLogFile(BaseTestClass):

    mock = Mock()

    def test_NormalCases(self):

        res = self.logOrganizer.isLogFile("fisher.log")
        self.assertEqual(res,True)

        res = self.logOrganizer.isLogFile("d.log")
        self.assertEqual(res,True)

        res = self.logOrganizer.isLogFile("slayer_log.log")
        self.assertEqual(res,True)

        res = self.logOrganizer.isLogFile("fisher_log_12_10_10.log")
        self.assertEqual(res,True)

        res = self.logOrganizer.isLogFile("fsdfsdfbnHIBFIaisdfnunfniuiafsdfsdfsdfsdfsdfsdfsdfsdfsdfnjsdnfjsdjlkfhikfinjkfi13uui1h4unhfuiauifasdpfnsdjinfnsdfnjsdjfjsdfpsdpfsdppodfgodfognjodfjhgdfhuohjosdnfuoisdhuofhsduoifhuoisdoifsr09iq3jirofnsdop02crjweuoinu9apfrha98whfu9nhaweu9ihfu9awenjfa8f9naweoipfj8aweipnjfie0awhf0ipec098run83qvfrnhu93vrnhfu9hwvnhru9awecfmh48-cxmyh-8rh-83nhry0m9rancyr9yaw3cbr2379vbnr79qv2307ryn0w3vyr7vaw3bn70avn7v9an0yv9avb79rbyavbna9vy0a098bn.log")
        self.assertEqual(res,True)

        # res = self.logOrganizer.isLogFile("")
        # self.assertEqual(res,)
        
    def test_CornerCases(self):

        res = self.logOrganizer.isLogFile(".log")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("fisher.lo")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("gjeaoijfoiawejfowamn")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("fisher")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("000000000")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("")
        self.assertEqual(res,False)

        res = self.logOrganizer.isLogFile("fisher_log")
        self.assertEqual(res,False)

        # res = self.logOrganizer.isLogFile("")
        # self.assertEqual(res,False)

        with self.assertRaises(TypeError):
            self.logOrganizer.isLogFile(111)
        with self.assertRaises(TypeError):
            self.logOrganizer.isLogFile(None)
        with self.assertRaises(TypeError):
            self.logOrganizer.isLogFile(self.mock)
        with self.assertRaises(TypeError):
            self.logOrganizer.isLogFile(True)
        with self.assertRaises(TypeError):
            self.logOrganizer.isLogFile(False)

        # with self.assertRaises():
        #     self.logOrganizer.isLogFile()

class TestCheckForLogs(BaseTestClass):

    def setUp(self):
        self.logOrganizer = LogOrganizer('test')

    def test_checkForLogsWithLogFiles(self):
        with patch.object(self.logOrganizer, 'items', ['fisher.log','fishers-logs']):
            self.assertTrue(self.logOrganizer.checkForLogs())

    def test_checkForLogsWithOutLogFiles(self):
        with patch.object(self.logOrganizer,'items',['file1.txt', 'file2.doc', 'file3.pdf', 'fishers-logs']):
            self.assertFalse(self.logOrganizer.checkForLogs())

if __name__ == "__main__":
    unittest.main()