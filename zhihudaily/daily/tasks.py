#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import timedelta

from celery.decorators import periodic_task

from .crawl import zhihu
from .crawl import fetch
from .models import News


@periodic_task(run_every=timedelta(hours=2))
def get_latest_news(date_str=None):
    print '==> get_latest_news'
    zh = zhihu.ZhiHu()
    latest_news = zh.get_latest_news()

    latest_news_ids = fetch.extract_news_ids(latest_news)

    date_str = fetch.extract_date_str(latest_news)

    for id in latest_news_ids:
        if News.objects.filter(news_id=id).exists():
            continue
        news = zh.get_news(id)
        news_obj, _ = News.objects.get_or_create(
            news_id=id,
            date=date_str,
            title=news['title'],
            share_url=news['share_url'],
            image_source=news['image_source']
        )
        image_name, image = fetch.fetch_image(news['share_url'], news['image'])
        news_obj.image.save(image_name, image)
