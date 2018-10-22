import unittest
import json
import os, sys
from endpoint import *
from sql_statements import *

class unit_testing(unittest.TestCase):

    def test_content_from_post(self):
        print("Testing test_content_from_post")
        expected = "Henrietta er swag"
        post_dict = posts()
        self.assertEquals(expected, post_dict[0]["content"])

    def test_create_post(self):
        print("Testing test_create_post")
        expected = '''{
        "post_type":"story",
        "username":"orvur",
        "pwd_hash":"1234",
        "post_title":"Største noob i verden",
        "hanesst_id":99999,
        "post_url":"https://www.facebook.com/orvurguttesen"}'''
        post_json = json.load(expected)
        create_post(post_json)
        post_id = find_post_with_hanesst_id(99999)
        self.assertTrue(post_id)

if __name__ == '__main__':
    unittest.main()