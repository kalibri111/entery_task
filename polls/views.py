from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import *
from .forms import PoolChoiceForm


class Rezult:
    def __init__(self, choice, value):
        self.choice = choice
        self.voters_percent = value


class PollsList(LoginRequiredMixin, generic.ListView):
    model = Question
    paginate_by = 10
    login_url = '/entery/accounts/login/'
    template_name = 'question_list.html'


class PoolDetail(LoginRequiredMixin, generic.DetailView):
    model = Question
    login_url = '/entery/accounts/login/'
    template_name = 'question_detail.html'

    def post(self, request, *args, **kwargs):
        this = get_object_or_404(Question, pk=self.kwargs['pk'])
        form_inst = PoolChoiceForm(data=request.POST, question=this)
        if form_inst.is_valid():
            choices = form_inst.cleaned_data['choices']  # titles
            voters = [obj.user for obj in Voters.objects.filter(question__exact=this)]
            if request.user in voters:
                return render(request, 'question_detail.html', {'error_message': 'Вы уже голосовали'})
            for choice_text in choices:
                tmp = Choice.objects.filter(choice_text__exact=choice_text, question__exact=this)[0]
                tmp.votes += 1
                tmp.save()
            Voters.objects.create(user=request.user, question=this)
        return redirect('poll-rezult', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(PoolDetail, self).get_context_data()
        this = get_object_or_404(Question, pk=self.kwargs['pk'])
        context['form'] = PoolChoiceForm(question=this)
        return context


class PoolRezult(LoginRequiredMixin, generic.DetailView):
    model = Question
    login_url = '/entery/accounts/login/'
    template_name = 'question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PoolRezult, self).get_context_data()
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        choices = Choice.objects.filter(question__exact=question)
        all_voters_value = 0
        for choice in choices:
            all_voters_value += choice.votes
        if all_voters_value:
            context['rezult_list'] = [
                Rezult(choice.choice_text, choice.votes * 100 / all_voters_value) for choice in choices
            ]
        return context

