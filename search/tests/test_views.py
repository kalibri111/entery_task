from django.test import TestCase
from event_manager.models import *


class EventSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_username', password='1234')
        Event.objects.create(header='test_search_header', description='test_description',
                             owner=User.objects.filter(username__exact='test_username')[0])

    def setUp(self) -> None:
        self.client.login(username='test_username', password='1234')

    def test_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_searched_header_exist(self):
        response = self.client.get('/entery/search/?event_header=test_search_header')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event_list'][0].header, 'test_search_header')

    def test_searched_header_does_not_exist(self):
        response = self.client.get('/entery/search/?event_header=header')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'event_list')

