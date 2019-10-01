from django.conf.urls import url, include
from django.urls import path

from hasker import views

urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
     path('signup/', views.signup, name='signup'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('profile/', views.profile, name='profile'),
     path('ask/', views.ask, name='ask'),
     path('questions/<int:question_id>', views.QuestionDetails.as_view(), name='question'),
     path('questions/<int:question_id>/votes/', views.QuestionVotesView.as_view(),
          name='question_votes'),
     path('answers/<int:answer_id>/select/', views.select_answer,
          name='select_answer'),
     path('answers/<int:answer_id>/votes/', views.AnswerVotesView.as_view(),
          name='answer_votes'),
     path('search/', views.search, name='search'),
     path('api/', include('hasker.api.urls')),
]
