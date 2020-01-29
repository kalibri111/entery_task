from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EventSearchView.as_view(), name='event-search'),
]
