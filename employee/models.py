from django.contrib.auth.models import User
from django.db import models
from event_manager.models import Member


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    sum = models.IntegerField(default=0)
