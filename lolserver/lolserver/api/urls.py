from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summoner/', views.summoner, name='summoner'),
    url(r'^champion/', views.champion, name='champion')
]