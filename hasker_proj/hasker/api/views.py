from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins

from ..models import Question, Tag, Answer
from .serializers import QuestionSerializer, TagSerializer, AnswerSerializer

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
