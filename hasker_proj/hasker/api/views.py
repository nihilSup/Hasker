from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action

from ..models import Answer, Question, Tag
from .serializers import AnswerSerializer, QuestionSerializer, TagSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def paged_response(self, objs):
        page = self.paginate_queryset(objs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(objs, many=True)
            return Response(serializer.data)

    @action(detail=False)
    def search(self, request):
        query = request.GET.get('search_query')
        questions = Question.search(query)
        
        return self.paged_response(questions)

    @action(detail=False)
    def ordered(self, request):
        field_name = request.GET.get('sortby')
        if field_name not in ('-asked_date', '-votes'):
            field_name = '-asked_date'
        questions = Question.objects.order_by(field_name)

        return self.paged_response(questions)

    @action(detail=False)
    def trending(self, request):
        return self.paged_response(Question.trending())

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
