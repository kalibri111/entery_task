from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_action, name='logout_action'),
    path('events/', views.EventDetailView, name='events'),
    path('<int:pk>/join/', views.event_join, name='joining'),
    url(r'^(?P<pk>\d+)$', views.EventDetailView.as_view(), name='event-detail'),
]
