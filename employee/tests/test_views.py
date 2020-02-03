from django.test import TestCase
from employee.models import *
from event_manager.models import *


class EmployeeAccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_user', password='1234')
        Event.objects.create(header='test_header', description='description', owner=User.objects.all()[0])
        Member.objects.create(user=User.objects.all()[0], event=Event.objects.all()[0])
        Payment.objects.create(member=Member.objects.all()[0], sum=123)

    def setUp(self) -> None:
        self.client.login(username='test_user', password='1234')

    def test_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'test_header')


class UserEventsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_user', password='1234')
        Event.objects.create(header='test_header', description='description', owner=User.objects.all()[0])
        Member.objects.create(user=User.objects.all()[0], event=Event.objects.all()[0])

    def setUp(self) -> None:
        self.client.login(username='test_user', password='1234')

    def test_logged_in(self):
        response = self.client.get(reverse('profile-events'))
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        response = self.client.get(reverse('profile-events'))
        self.assertContains(response, 'test_header')
