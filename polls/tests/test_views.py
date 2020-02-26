from django.test import TestCase
from ..forms import *
from event_manager.models import *
from django.shortcuts import get_object_or_404


class PoolDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_username', password='1234')
        Question.objects.create(question_title='test_title', question_text='test_text')
        Choice.objects.create(question=get_object_or_404(Question, pk=1), choice_text='test_choice')

    def setUp(self) -> None:
        self.client.login(username='test_username', password='1234')

    def test_logged_in(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_post_first_vote(self):
        resp = self.client.post(reverse('pool-detail', kwargs={'pk': 1}), {'choices': 'test_choice'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(Voters.objects.all()), 1)
        voter = Voters.objects.filter(user__username__exact='test_username')[0]
        self.assertEqual(voter.user,
                         User.objects.filter(username__exact='test_username')[0])
        self.assertEqual(voter.question, Question.objects.filter(question_title__exact='test_title')[0])

    def test_post_already_vote(self):
        self.test_post_first_vote()
        resp = self.client.post(reverse('pool-detail',  kwargs={'pk': 1}), {'choices': 'test_choice'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['error_message'], 'Вы уже голосовали')
        self.assertEqual(len(Voters.objects.all()), 1)

    def test_get_context_data(self):
        resp = self.client.get(reverse('pool-detail', args=[1]))
        context = resp.context
        self.assertTrue(isinstance(context['form'], PoolChoiceForm))


class PollRezultTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Question.objects.create(question_title='test_title', question_text='test_text')
        Choice.objects.create(question=get_object_or_404(Question, pk=1), choice_text='test_choice_1', votes=1)
        Choice.objects.create(question=get_object_or_404(Question, pk=1), choice_text='test_choice_2', votes=3)

    def test_get_context_data(self):
        resp = self.client.get(reverse('poll-rezult', kwargs={'pk': 1}))
        rez_list = resp.context['rezult_list']
        self.assertEqual(len(rez_list), 2)
        self.assertEqual(rez_list[0].voters_percent, 25.0)
        self.assertEqual(rez_list[1].voters_percent, 75.0)
