from django.conf.urls import url

from hasker import views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
]
