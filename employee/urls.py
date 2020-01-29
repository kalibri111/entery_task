from django.urls import path
from . import views


urlpatterns = [
    path('', views.EmployeeAccountView.as_view(), name='profile'),
    path('my-events/', views.UserEventsView.as_view(), name='profile-events'),
]
