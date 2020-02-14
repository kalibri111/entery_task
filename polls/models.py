from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Question(models.Model):
    question_title = models.TextField(max_length=255)
    question_text = models.TextField(max_length=1024)

    def __str__(self):
        return self.question_title

    def get_absolute_url(self):
        return reverse('pool-detail', args=[str(self.id)])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="contains")
    choice_text = models.TextField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        unique_together = ['choice_text', 'question']


class Voters(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    choices = models.ForeignKey(Choice, on_delete=models.CASCADE)
