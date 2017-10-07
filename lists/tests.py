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

    def test_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item1", item_list=correct_list)
        Item.objects.create(text="item2", item_list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item1", item_list=other_list)
        Item.objects.create(text="other list item2", item_list=other_list)

        responce = self.client.get('/lists/{0}/'.format(correct_list.id))

        self.assertContains(responce, 'item1')
        self.assertContains(responce, 'item2')
        self.assertNotContains(responce, 'other list item1')
        self.assertNotContains(responce, 'other list item2')        

    def test_uses_list_template(self):
        list_ = List.objects.create()
        responce = self.client.get('/lists/{0}/'.format(list_.id))
        self.assertTemplateUsed(responce, 'lists/list.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        responce = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(responce, '/lists/{0}/'.format(new_list.id))

    def test_can_save_POST_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post('/lists/{0}/add'.format(correct_list.id),
        data={'item_text': 'A new item for existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.item_list, correct_list)

    def test_redirecs_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        responce = self.client.post('/lists/{0}/add'.format(correct_list.id),
        data={'item_text': 'A new item for existing list'})
        self.assertRedirects(responce, '/lists/{0}/'.format(correct_list.id))

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)