import unittest
from api.endpoint import sort_posts

class unit_testing(unittest.TestCase):

    def test_content_from_post(self):
        expected = "Henrietta er swag"
        post_dict = sort_posts()
        self.assertTrue(expected in post_dict)

if __name__ == '__main__':
    unittest.main()