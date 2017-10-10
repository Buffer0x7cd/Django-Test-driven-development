from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip
from selenium.common.exceptions import WebDriverException
import time

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        ''' Edith goes to the home page and accidentally tries to submit
        an empty list item. She hits Enter on the empty input box '''
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)

        ''' The home page refreshes, and there is an error message saying
        that list items cannot be blank'''

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "you can't submit empty list items"
        ))

        ''' She tries again with some text for the item, which now works'''
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: buy milk')

        '''  she tries to enter a blank line again'''
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        ''' again she recieves an error message'''
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "you can't submit empty list items"
        ))
        ''' and she can correct it by filling some text in'''
        inputbox =  self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy mango')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: buy milk')
        self.check_for_row_in_list_table('2: buy mango')
        self.fail('Finish this test')

