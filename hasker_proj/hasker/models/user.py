from django.contrib.auth.models import AbstractUser
from django.db import models


class HaskerUser(AbstractUser):

    avatar = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return super().username
