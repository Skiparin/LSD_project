#!/usr/bin/env python

import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class TestUbuntuHomepage(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options, executable_path="/usr/bin/geckodriver")

    def testTitle(self):
        self.browser.get('http://www.ubuntu.com/')
        self.assertIn('Ubuntu', self.browser.title)

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
