import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        table = self.browser.find_element_by_id('list-table')
        rows = table.find_elements_by_tag_name('tr')

        # check if our inserted item exists in the rows
        self.assertIn('1: Buy peacock feathers',
            [row.text for row in rows]
        )

        # enter another item into the textbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # table of to-do items, and its rows
        table = self.browser.find_element_by_id('list-table')
        rows = table.find_elements_by_tag_name('tr')

        # check if our second inserted item exists in the rows
        self.assertIn('2: Use peacock feathers to make a fly',
            [row.text for row in rows]  
        )

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
