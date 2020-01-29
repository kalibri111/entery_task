from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.models import *


class EmployeeAccountView(LoginRequiredMixin, generic.ListView):
    model = Payment
    template_name = 'user_account.html'
    context_object_name = 'payment_info'

    login_url = '/entery/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super(EmployeeAccountView, self).get_context_data()
        data = Payment.objects.filter(member__user=self.request.user).values('member__event__header')
        to_context = []
        for header in data:
            to_context.append(header['member__event__header'])
        context['events'] = to_context
        return context


class UserEventsView(LoginRequiredMixin, generic.ListView):
    model = Member
    template_name = 'user_events.html'
    context_object_name = 'user_events'
    login_url = '/entery/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super(UserEventsView, self).get_context_data()
        events = Member.objects.filter(user__exact=self.request.user).values('event__header')
        context['joined_events'] = []

        for event in events:
            context['joined_events'].append(event['event__header'])
        return context
