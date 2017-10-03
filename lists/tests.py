from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
class HomePageTest(TestCase):
    ''' Test if home page is accessible'''
    def test_root_url_resolve_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        responce = home_page(request)
        html = responce.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
