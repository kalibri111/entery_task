from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import *
from .forms import PoolChoiceForm


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
                Choice.objects.filter(choice_text__exact=choice_text, question__exact=this)[0].votes += 1
            Voters.objects.create(user=request.user, question=this)
        return redirect('polls-list')

    def get_context_data(self, **kwargs):
        context = super(PoolDetail, self).get_context_data()
        this = get_object_or_404(Question, pk=self.kwargs['pk'])
        context['choices_list'] = Choice.objects.filter(question__exact=this)
        context['form'] = PoolChoiceForm(question=this)
        return context

