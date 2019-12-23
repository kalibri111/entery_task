from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Event, Employee, Member, User
from .forms import UserForm, MemberForm
from django.views import generic
from django.views import View


class Home(View):
    """
    user page view
    """

    def get(self, request):
        context = {
            'user_first_name': request.user.first_name,
            'user_last_name': request.user.last_name,
            'department': Employee.objects.filter(user__exact=request.user).values()[0]['department'],
            'event_list': Event.objects.all(),
        }
        return render(request, 'home.html', context)

    def post(self, request):
        if 'logout-button' in request.POST:
            logout(request)
            return redirect('index')


class EventDetailView(generic.DetailView):
    """
    view event detail
    """
    model = Event
    form_class = MemberForm
    context_object_name = 'event_detail'
    template_name = 'event_detail.html'

    def post(self, request, pk):
        if 'submit-button' in request.POST:
            current_user = User.objects.filter(id__exact=request.user.id)[0]
            current_employee = Employee.objects.filter(user__exact=current_user)[0]
            member = Member(employee=current_employee, event=Event.objects.get(pk=pk))
            if not (Member.objects.filter(employee__exact=member.employee, event__exact=member.event)):
                member.save()
                if member.event.is_limited:
                    ptr = Member.objects.get(employee__exact=member.employee, event__exact=member.event)
                    ptr.event.vacant_places = int(ptr.event.vacant_places) - 1
                    ptr.save()
                return redirect('rezult', 'ok')
            else:
                return redirect('rezult', 'error')


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        return render(request, self.template_name, {'forms': form})


class MemberFormView(View):
    form_class = MemberForm
    template_name = 'event_detail.html'

    def post(self, request, pk):
        form = self.form_class(request.POST)
        member = Member(user=request.user, event=Event.objects.get(pk=pk))
        member.save()
        return redirect('event-detail')

    def get(self, request, pk):
        form = self.form_class(request.POST)
        return render(request, self.template_name, {'forms': form})


class TakePartView(View):

    def get(self, request, rezult):
        return render(request, 'rezult.html', {'rezult': rezult})
