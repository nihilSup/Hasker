from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class HaskerUser(AbstractUser):

    avatar = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return super().username


UserModel = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    asked_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    up_votes = models.ManyToManyField(UserModel, blank=True,
                                      related_name='question_up')
    down_votes = models.ManyToManyField(UserModel, blank=True,
                                        related_name='question_down')

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    answered_date = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    up_votes = models.ManyToManyField(UserModel, blank=True,
                                      related_name='answer_up')
    down_votes = models.ManyToManyField(UserModel, blank=True,
                                        related_name='answer_down')

    def qual_name(self):
        return f"{self.__class__.__name__}_{self.id}"
