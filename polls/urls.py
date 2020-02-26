from django.urls import path
from .views import *
from django.conf.urls import url


urlpatterns = [
    path('', PollsList.as_view(), name='polls-list'),
    url(r'^(?P<pk>\d+)$', PoolDetail.as_view(), name='pool-detail'),
    url(r'^rezult/(?P<pk>\d+)$', PoolRezult.as_view(), name='poll-rezult'),
]
