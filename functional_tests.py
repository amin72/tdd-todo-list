import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_starting_a_new_todo_list(self):

        self.browser.get('http://127.0.0.1:8000/')

        # our project is a todolist, so To-Do must in the title of /
        self.assertIn('To-Do', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
