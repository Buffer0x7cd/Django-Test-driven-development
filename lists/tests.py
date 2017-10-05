from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item


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


class ItemModelTest(TestCase):
    ''' Test the item model'''

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')