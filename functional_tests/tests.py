import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase


MAX_WAIT = 20

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_starting_a_new_todo_list(self):
        '''Some tests on todo list index page'''

        self.browser.get(self.live_server_url)

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

        # save current url
        old_list_url = self.browser.current_url
        # check if url is matched
        self.assertRegex(old_list_url, '/lists/.+') # eg: /lists/1

        # close browser, cuase we're going to let another user use our website
        self.browser.quit()
        # now reopen the browser
        self.browser = webdriver.Firefox()

        # new user visits host page, he can not see others to-do items
        # so there will be no items in home page.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        import time; time.sleep(5)

        # save new url
        new_list_url = self.browser.current_url
        # check if url is matched
        self.assertRegex(new_list_url, '/lists/.+') # eg: /lists/2
        # check old and new urls, they must be different urls
        self.assertNotEqual(new_list_url, old_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


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
