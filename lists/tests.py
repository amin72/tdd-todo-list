import re
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Item, List


def remove_csrf(html_code):
    '''
        Remove CSRF Token.
        On each request csrf token is renewed,
        So with this method we can get rid of csrf tokens.
    '''
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_code)



class HomePageTest(TestCase):
    
    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

        # check if expected content is equal to response content
        expected_content = render_to_string('lists/home.html', request=request)
        expected_content = remove_csrf(expected_content)
        response_content = remove_csrf(response.content.decode())
        self.assertEqual(response_content, expected_content)


    def test_home_page_shows_items_in_database(self):
        list_ = List.objects.create()
        Item.objects.create(text='item 1', list=list_)
        Item.objects.create(text='item 2', list=list_)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())



class NewListViewText(TestCase):

    def test_home_page_can_save_post_requests_to_database(self):
        self.client.post('/lists/new/', {'item_text': 'A new item'})
        item_from_db = Item.objects.all()[0]
        self.assertEqual(item_from_db.text, 'A new item')

    
    def test_redirects_to_list_url(self):
        response = self.client.post('/lists/new/', {'item_text': 'A new item'})
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')



class ListViewTest(TestCase):
    
    def test_lists_page_shows_items_in_database(self):
        our_list = List.objects.create()
        Item.objects.create(text='item 1', list=our_list)
        Item.objects.create(text='item 2', list=our_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='not this one', list=other_list)

        response = self.client.get(f'/lists/{our_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'not this one')


    def test_uses_lists_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')


    def test_passes_list_to_template(self):
        our_list = List.objects.create()
        response = self.client.get(f'/lists/{our_list.id}/')
        self.assertEqual(response.context['list'], our_list)



class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items_to_the_database(self):
        first_list = List.objects.create()
        first_item = Item()
        first_item.text = 'Item the first'
        first_item.list = first_list
        first_item.save()

        second_item = Item()
        second_item.text = 'second item'
        second_item.list = first_list
        second_item.save()

        first_item_from_db = Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, 'Item the first')
        self.assertEqual(first_item_from_db.list, first_list)

        second_item_from_db = Item.objects.all()[1]
        self.assertEqual(second_item_from_db.text, 'second item')
        self.assertEqual(second_item_from_db.list, first_list)



class AddItemToExistingListTest(TestCase):

    def test_adding_an_item_to_an_existing_list(self):
        our_list = List.objects.create()
        self.client.post(f'/lists/{our_list.id}/add/',
            {'item_text': 'new item for my list'})
        
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, our_list)
        self.assertEqual(new_item.text, 'new item for my list')

    
    def test_redirects_to_list_page(self):
        List.objects.create() # create another list
        # and create our list.
        # redirection must go to our list page and not the other list
        our_list = List.objects.create()
        response = self.client.post(f'/lists/{our_list.id}/add/',
            {'item_text': 'new item for my list'})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/lists/{our_list.id}/')
