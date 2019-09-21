from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import AnswerViewSet, QuestionViewSet, TagViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'tags', TagViewSet)
router.register(r'answers', AnswerViewSet)


urlpatterns = router.urls
urlpatterns += [
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
            template_name='hasker/swagger-ui.html',
            extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
