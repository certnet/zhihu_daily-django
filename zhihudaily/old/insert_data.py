#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

import django
django.setup()

from daily.crawl import zhihu
from daily.crawl import fetch
from daily.models import News


if __name__ == "__main__":
    zh = zhihu.ZhiHu()
    latest_news = zh.get_latest_news()
    print json.dumps(latest_news, ensure_ascii=False, indent=2)

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
