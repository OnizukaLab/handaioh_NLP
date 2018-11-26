from django.db import models

# Create your models here.

class Quiz(models.Model):
    # ニュース文
    text = models.TextField(default='')
    title = models.TextField(default='')
    blank_cand = models.TextField(default='')
    second_text = models.TextField(default='')
    date_inf = models.DateTimeField('date published')
    favorite_count = models.IntegerField(default=-1)
    retweet_count = models.IntegerField(default=-1)


