from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^creat_question/', views.creat_question, name='creat_question'),
]