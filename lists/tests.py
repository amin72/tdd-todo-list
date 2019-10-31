from django.test import TestCase
from django.http import HttpRequest

from .views import home_page

class HomePageTest(TestCase):
    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

        with open('lists/templates/lists/home.html') as f:
            expected_content = f.read()

        self.assertEqual(response.content.decode('latin-1'), expected_content)
