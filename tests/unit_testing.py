import unittest
import json
import os, sys
from unittest.mock import patch
parentPath = os.path.abspath("../api")
if parentPath not in sys.path:
    sys.path.insert(0,parentPath)
from endpoint import posts #, create_post
from sql_statements import *#find_post_with_hanesst_id

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
        post_json = json.loads(expected)
        create_post(post_json)
        post_id = find_post_with_hanesst_id(99999)
        self.assertTrue(post_id)

     def test_create_comment(self):
        print("Testing test_create_comment")
        expected = '''{
        "post_type":"comment",
        "username":"orvur2",
        "pwd_hash":"1234",
        "post_title":"Candy Crush Friends sucks",
        "hanesst_id":100000,
        "post_url":"https://www.facebook.com/orvurguttesen"}'''
        comment_json = json.loads(expected)
        create_comment(comment_json)
        comment_id = find_comment_with_hanesst_id(100000)
        self.assertTrue(comment_id)


if __name__ == '__main__':
    unittest.main()