import re
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page


class HomePageTest(TestCase):
    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

        # check if expected content is equal to response content
        expected_content = render_to_string('lists/home.html', request=request)
        expected_content = HomePageTest.remove_csrf(expected_content)
        response_content = HomePageTest.remove_csrf(response.content.decode())
        self.assertEqual(response_content, expected_content)

    @staticmethod
    def remove_csrf(html_code):
        '''
            Remove CSRF Token.
            On each request csrf token is renewed,
            So with this method we can get rid of csrf tokens.
        '''
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)
