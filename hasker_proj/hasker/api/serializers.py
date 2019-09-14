from rest_framework import serializers

from ..models import Question, Answer, Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ('url', 'author', 'answered_date', 'content', 'is_correct', 'question')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = TagSerializer(read_only=True, many=True)
    answers = AnswerSerializer(read_only=True, many=True, source='answer_set')
    
    class Meta:
        model = Question
        fields = ('url', 'author', 'title', 'votes', 'asked_date', 'content', 'answers', 'tags')
