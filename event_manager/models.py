from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    created = models.DateTimeField(auto_now_add=True)
    header = models.TextField(max_length=100)
    description = models.TextField(max_length=1000)
    short_description = models.TextField(max_length=1000, null=True)
    vacant_places = models.IntegerField(null=True)
    is_limited = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through='Member')

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Member(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def join_member(user, event):
        if event.is_limited:
            places = int(event.vacant_places)
            if places > 0:
                member = Member.objects.create(user=user, event=event)
                try:
                    member.save()
                except IntegrityError:
                    raise IntegrityError
                else:
                    places -= 1
                    member.event.vacant_places = places
                    member.event.save()
        else:
            member = Member.objects.create(user=user, event=event)
            try:
                member.save()
            except IntegrityError:
                raise IntegrityError
            else:
                member.event.save()

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + self.event.header

