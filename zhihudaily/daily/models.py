from __future__ import unicode_literals

from django.db import models


class News(models.Model):
    news_id = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    title = models.CharField(max_length=256)
    share_url = models.CharField(max_length=256)
    image = models.FileField(upload_to='daily/%Y-%m-%d')
    image_source = models.CharField(max_length=256)
