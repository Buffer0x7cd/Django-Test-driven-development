from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        ''' Check if correct template is being used for render'''
        responce = self.client.get('/')
        self.assertTemplateUsed(responce, 'lists/home.html')

class ListAndItemModelTest(TestCase):
    ''' Test the item model'''

    def test_saving_and_retrieving_items(self):
        list_ =  List()
        list_.save()
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.item_list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.item_list = list_
        second_item.save()

        saved_lists = List.objects.first()
        self.assertEqual(saved_lists, list_)


        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.item_list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.item_list, list_)


class LiveViewTest(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="item1", item_list=list_)
        Item.objects.create(text="item2", item_list=list_)

        responce = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(responce,'item1')
        self.assertContains(responce ,'item2')

    def test_uses_list_template(self):
        responce = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(responce, 'lists/list.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        responce = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(responce, '/lists/the-only-list-in-the-world/')
