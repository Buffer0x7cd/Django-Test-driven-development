from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        ''' Check if correct template is being used for render'''
        responce = self.client.get('/')
        self.assertTemplateUsed(responce, 'lists/home.html')
        
    def test_can_save_a_POST_request(self):
        ''' Test if view echo back the post data'''
        responce = self.client.post('/', data={
            'item_text': 'A new list item'
        })
        self.assertIn('A new list item', responce.content.decode())
        self.assertTemplateUsed(responce, 'lists/home.html')