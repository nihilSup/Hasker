from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action

from ..models import Answer, Question, Tag
from .serializers import AnswerSerializer, QuestionSerializer, TagSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False)
    def search(self, request):
        query = request.GET.get('search_query')
        questions = Question.search(query)
        
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
