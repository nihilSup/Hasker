from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, TagViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'tags', TagViewSet)
router.register(r'answers', AnswerViewSet)


urlpatterns = router.urls