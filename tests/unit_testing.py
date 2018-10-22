import unittest
import os, sys
from unittest.mock import patch
parentPath = os.path.abspath("../api")
if parentPath not in sys.path:
    sys.path.insert(0,parentPath)
from endpoint import posts

class unit_testing(unittest.TestCase):

    def test_content_from_post(self):
        expected = "Henrietta er swag"
        post_dict = posts()
        self.assertTrue(expected in post_dict)

if __name__ == '__main__':
    unittest.main()