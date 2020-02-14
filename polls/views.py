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
        form_inst = PoolChoiceForm(request.POST)
        # id = request.POST.get('id')
        # form_inst.fields['unit_id'].choices = [(id, id)]
        print(form_inst.fields)
        if form_inst.is_valid():
            a = form_inst.cleaned_data['choices']
        return render(request, 'question_detail.html', {'form': form_inst})

    def get_context_data(self, **kwargs):
        context = super(PoolDetail, self).get_context_data()
        this = get_object_or_404(Question, pk=self.kwargs['pk'])
        context['choices_list'] = Choice.objects.filter(question__exact=this)
        context['form'] = PoolChoiceForm.question_constructor(this)
        return context

