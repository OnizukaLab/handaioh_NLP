from django.urls import path
from . import views
from django.conf.urls import url, include
from .views import QuizViewSet
from rest_framework import routers




urlpatterns = [
    url(r'^create_question/', views.create_question, name='create_question'),
    url('api/', QuizViewSet.as_view(), name='quiz-get'),
]
