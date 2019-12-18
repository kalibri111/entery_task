from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    url(r'^/(?P<book_id>\d+)$', views.EventDetailView.as_view(), name='event-detail')
]
