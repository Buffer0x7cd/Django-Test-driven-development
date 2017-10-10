from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    
    def test_cannot_add_empty_list_items(self):
        ''' some story '''
        self.fail('write me')