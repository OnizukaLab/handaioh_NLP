from django.db import models

# Create your models here.

class Quiz(models.Model):
    # ニュース文
    text = models.TextField()
    # 日時
    date_inf = models.DateTimeField('date published')

