#!/usr/bin/env python

import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import unittest

class TestUbuntuHomepage(unittest.TestCase):

    #Setting up the driver in headless mode
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")

        cls.driver = webdriver.Firefox(options=options, executable_path="/usr/bin/geckodriver")
        cls.driver.get("http://159.65.116.24:5004/sortedposts")

    #This returns us to the start page every time a test finished.
    def tearDown(self):
        self.driver.get("http://159.65.116.24:5004/sortedposts")

    #Closing the driver when we are finnished testing.
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_get_posts(self):
        print("test get posts")
        self.result = self.driver.find_element_by_xpath("//tr[@class='athing']/td/span").text
        self.expected = 1
        self.assertEqual(self.result, self.expected)

if __name__ == '__main__':
    unittest.main()
