from django.conf.urls import url
from django.urls import path

from hasker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^ask/$', views.ask, name='ask'),
    path(r'questions/<int:question_id>', views.question, name='question'),
    path(r'questions/<int:question_id>/votes/', views.question_votes,
         name='question_votes')
]
