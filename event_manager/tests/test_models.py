from django.test import TestCase
from event_manager.models import *
from django.db import transaction


class MemberTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test_username', first_name='test_first_name',
                                             last_name='test_last_name')
        test_user.save()
        owner = User.objects.create_user(username='owner', first_name='owner_test_first_name',
                                         last_name='owner_test_last_name')
        owner.save()

    def test_join_member_member_event_isnt_limited(self):
        owner = User.objects.filter(username__exact='owner')[0]
        test_event = Event.objects.create(description='test', header='test', is_limited=False, owner=owner)
        test_event.save()
        test_user = User.objects.filter(username__exact='test_username')[0]
        Member.join_member(test_user, test_event)
        self.assertEqual(Member.objects.all()[0].user, test_user)
        self.assertEqual(Member.objects.all()[0].event, test_event)

    def test_join_member_vacant_places_exist(self):
        owner = User.objects.filter(username__exact='owner')[0]
        test_event = Event.objects.create(description='test', header='test', is_limited=True, vacant_places=2,
                                          owner=owner)
        test_event.save()
        test_user = User.objects.filter(username__exact='test_username')[0]
        Member.join_member(test_user, test_event)
        self.assertEqual(Member.objects.all()[0].user, test_user)
        self.assertEqual(Member.objects.all()[0].event, test_event)
        self.assertEqual(Member.objects.all()[0].event.vacant_places, 1)

    def test_join_member_vacant_places_not_exist(self):
        owner = User.objects.filter(username__exact='owner')[0]
        test_event = Event.objects.create(description='test', header='test', is_limited=True, vacant_places=0,
                                          owner=owner)
        test_event.save()
        test_user = User.objects.filter(username__exact='test_username')[0]
        Member.join_member(test_user, test_event)
        self.assertEqual(len(Member.objects.all()), 0)

    def test_join_member_already_exist(self):
        owner = User.objects.filter(username__exact='owner')[0]
        test_event = Event.objects.create(description='test', header='test', is_limited=True, vacant_places=3,
                                          owner=owner)
        test_event.save()
        test_user = User.objects.filter(username__exact='test_username')[0]
        Member.join_member(test_user, test_event)
        self.assertEqual(len(Member.objects.all()), 1)
        try:
            with transaction.atomic():
                Member.join_member(test_user, test_event)
            self.fail('Member duplicates')
        except IntegrityError:
            pass
