from .models import Event, Employee
from django.views import generic


class Home(generic.ListView):
    """
    user page view
    """
    model = Employee, Event
    template_name = 'home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_first_name'] = Employee.user.first_name
        context['user_last_name'] = Employee.user.last_name
        context['department'] = Employee.department
        context['event_list'] = Event.objects.all()

    paginate_by = 20


class EventDetailView(generic.DetailView):
    """
    view event detail
    """
    model = Event
    template_name = 'event_detail.html'
