from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from django.core.exceptions import ValidationError

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

    def test_cannot_save_empty_items(self):
        list_= List.objects.create()
        item = Item(text='', item_list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()