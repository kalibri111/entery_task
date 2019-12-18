from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)


class Event(models.Model):
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='owner')
    created = models.DateTimeField(auto_now_add=True)
    header = models.TextField(max_length=100)
    description = models.TextField(max_length=1000)  # TODO set description length
    vacant_places = models.CharField(max_length=4, null=True)
    is_limited = models.BooleanField(default=True)
    members = models.ManyToManyField(Employee, through='Member')

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Member(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return self.sum
