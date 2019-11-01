import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 20

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_starting_a_new_todo_list(self):
        '''Some tests on todo list index page'''

        self.browser.get('http://127.0.0.1:8000/')

        # our project is a todolist, so To-Do must in the title of /
        self.assertIn('To-Do', self.browser.title)

        # there is a h1 header which contains To-Do
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)

        # there is an input element with id of id_new_item, and its placeholder
        # is equal to 'Enter a to-do item'
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
            'Enter a to-do item')

        # send an to-do item and press enter
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        # now todo list gets updated. and we can retreive new inserted item

        # table of to-do items, and its rows
        # check if our inserted item exists in the rows
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # enter another item into the textbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test')

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('list-table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(.5)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
