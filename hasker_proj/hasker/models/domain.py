import re

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

_UserModel = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Votable(models.Model):
    author = models.ForeignKey(_UserModel, on_delete=models.CASCADE)
    up_votes = models.ManyToManyField(_UserModel, blank=True,
                                      related_name='%(class)s_up')
    down_votes = models.ManyToManyField(_UserModel, blank=True,
                                        related_name='%(class)s_down')
    votes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def user_ups(self, user):
        return self.up_votes.filter(id=user.id).count()

    def user_downs(self, user):
        return self.down_votes.filter(id=user.id).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # smells, another solution with calc field denies order by
        self.votes = self.up_votes.count() - self.down_votes.count()
        super().save(update_fields=["votes"])

    @transaction.atomic
    def handle_new_vote(self, user, vote_type):
        if self.author == user:
            return None
        user_ups = self.user_ups(user)
        user_downs = self.user_downs(user)
        if vote_type == 'up':
            if user_ups == 0 and user_downs == 0:
                self.up_votes.add(user)
            elif user_ups == 0 and user_downs != 0:
                self.down_votes.remove(user)
        elif vote_type == 'down':
            if user_ups == 0 and user_downs == 0:
                self.down_votes.add(user)
            elif user_ups != 0 and user_downs == 0:
                self.up_votes.remove(user)
        self.save() 


class Question(Votable):
    title = models.CharField(max_length=128)
    content = models.TextField()
    asked_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)

    @classmethod
    def search(cls, query):
        if query is not None:
            match = re.match('tag:(\w+)$', query)
            if match:
                tag_name = match[1]
                matched_qs = cls.objects.filter(tags__name=tag_name)
            else:
                matched_qs = cls.objects.filter(Q(title__icontains=query) |
                                                Q(content__icontains=query))
        else:
            matched_qs = cls.objects.all()
        return matched_qs.order_by('-votes', '-asked_date')

    @classmethod
    def trending(cls, n=20):
        return Question.objects.all().order_by('-votes')[:n]

    def __str__(self):
        return self.title


class Answer(Votable):
    content = models.TextField()
    answered_date = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def qual_name(self):
        return f"{self.__class__.__name__}_{self.id}"
