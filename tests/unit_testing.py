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
        print(post_dict)
        self.assertEquals(expected, post_dict[0]["content"])

if __name__ == '__main__':
    unittest.main()