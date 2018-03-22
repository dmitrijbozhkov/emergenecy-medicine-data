""" Test that always passing """
import unittest

class TestDesign(unittest.TestCase):
    def test_pass(self):
        """ Always passes """
        self.assertTrue(True)
        return
    
    def test_fail(self):
        """ Always fails """
        self.assertTrue(False)
        return

if __name__ == '__main__':
    unittest.main()
