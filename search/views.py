from event_manager.models import Event
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from event_manager.forms import SearchForm


class EventSearchView(LoginRequiredMixin, generic.ListView):
    template_name = 'home.html'
    paginate_by = 10
    model = Event

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventSearchView, self).get_context_data()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            header_to_search = form.cleaned_data['field']
            if header_to_search is not None:
                searched = Event.objects.filter(header__exact=header_to_search)
                context['event_list'] = searched
        context['form'] = SearchForm()
        return context
