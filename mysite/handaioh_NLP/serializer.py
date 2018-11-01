# coding: utf-8

# データベースからニュース文を取得して，JSON形式でviews.pyに渡す

from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
