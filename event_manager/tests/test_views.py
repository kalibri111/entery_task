from django.test import TestCase
from event_manager.models import *


class LogoutActionTest(TestCase):

    def setUp(self) -> None:
        test_user = User.objects.create_user(username='test_username', password='1234')
        test_user.save()

    def test_logout_action(self):
        self.client.login(username='test_username', password='1234')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'test_username')
        response = self.client.get(reverse('logout_action'))
        self.assertNotContains(response, 'user', status_code=302)


class EventDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Test_username', first_name='Test_first_name', last_name='Test_last_name')
        Event.objects.create(header='Test_header', description='Test_description',
                             owner=User.objects.filter(first_name__exact='Test_first_name')[0])
        Member.objects.create(user=User.objects.filter(first_name__exact='Test_first_name')[0],
                              event=Event.objects.filter(header__exact='Test_header')[0])

    def setUp(self) -> None:
        test_user = User.objects.create_user(username='test_observer', password='1234')
        test_user.save()

    def test_get_context_data(self):
        self.client.login(username='test_observer', password='1234')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'test_observer')

        response = self.client.get(reverse('event-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['members_list'][0].first_name, 'Test_first_name')
        self.assertEqual(response.context['members_list'][0].last_name, 'Test_last_name')


class EventJoinTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Test_username', first_name='Test_first_name', last_name='Test_last_name')
        Event.objects.create(header='test_header', description='test_description',
                             owner=User.objects.filter(first_name__exact='Test_first_name')[0], is_limited=True,
                             vacant_places=2)

    def setUp(self) -> None:
        test_user = User.objects.create_user(first_name='test_user_first_name', last_name='test_user_last_name',
                                             username='test_username', password='1234')
        test_user.save()
        self.client.login(username='test_username', password='1234')

    def test_user_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'test_username')

    def test_successfully_added(self):
        response = self.client.post(reverse('joining', args=[1]))
        self.assertEqual(response.status_code, 302)
        new_member = Member.objects.filter(user__username__exact='test_username')[0]
        self.assertEqual(new_member.event.header, 'test_header')
        self.assertEqual(new_member.user.username, 'test_username')

    def test_already_exist(self):
        response = self.client.post(reverse('joining', args=[1]))
        response = self.client.post(reverse('joining', args=[1]))
        self.assertRaises(IntegrityError)
