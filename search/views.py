from django.shortcuts import render
from event_manager.models import Event
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin


class EventSearchView(LoginRequiredMixin, generic.ListView):
    template_name = 'home.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        context = {}
        event_name = request.GET.get('event_header')
        headers = [header['header'] for header in Event.objects.values('header')]
        if event_name is not None and event_name in headers:
            search_events = Event.objects.filter(header__exact=event_name)
            paginator = Paginator(search_events, 10)
            page = request.GET.get('page')
            try:
                context['event_list'] = paginator.page(page)
            except PageNotAnInteger:
                context['event_list'] = paginator.page(1)
            except EmptyPage:
                context['event_list'] = paginator.page(paginator.num_pages)
        return render(request, 'home.html', context)
