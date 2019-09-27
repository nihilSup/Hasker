from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class HaskerUser(AbstractUser):

    avatar = models.ImageField(upload_to='profile_images', blank=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static("hasker/images/default.png")

    def __str__(self):
        return super().username
