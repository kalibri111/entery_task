from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.views import generic
from event_manager.forms import *


def logout_action(request):
    logout(request)
    return redirect('index')


class Home(LoginRequiredMixin, generic.ListView):
    """
    user page view
    """
    model = Event
    template_name = 'home.html'
    login_url = '/entery/accounts/login/'
    form = SearchForm()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data()
        context['form'] = self.form
        return context


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    """
    view event detail
    """
    model = Event
    context_object_name = 'event_detail'
    template_name = 'event_detail.html'
    login_url = '/entery/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data()
        this_event = get_object_or_404(Event, pk=self.kwargs['pk'])
        members = this_event.members.all()
        context['members_list'] = members
        return context


def event_join(request, pk):
    if request.method == 'POST':
        current_user = request.user
        current_event = get_object_or_404(Event, pk=pk)
        try:
            Member.join_member(current_user, current_event)
        except IntegrityError:
            return render(request, 'event_detail.html',
                          context={'error_message': 'There is an error, are you already joined?', 'event_detail': [],
                                   'member_list': []})
        else:
            return redirect('index')
