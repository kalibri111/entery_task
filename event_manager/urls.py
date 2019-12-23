from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('/events/', views.EventDetailView, name='events'),
    url(r'^(?P<pk>\d+)$', views.EventDetailView.as_view(), name='event-detail'),
    url(r'^(?P<rezult>\w+)', views.TakePartView.as_view(), name='rezult')
]
