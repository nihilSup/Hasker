from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class HaskerUser(AbstractUser):

    avatar = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return super().username


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    asked_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answered_date = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
