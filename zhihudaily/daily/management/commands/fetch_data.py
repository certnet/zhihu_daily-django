#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json

from django.core.management.base import BaseCommand
#  from django.core.management.base import CommandError

from daily.crawl import zhihu
from daily.crawl import fetch
from daily.models import News


class Command(BaseCommand):
    help = 'print news title'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--cron',
            action='store_true',
            dest='cron',
            default=False,
            help=u'定时任务'
        )

    def handle(self, *args, **options):
        self.insert_data()
        if options.get('cron'):
            self.cron_run()

    def insert_data(self):
        zh = zhihu.ZhiHu()
        latest_news = zh.get_latest_news()
        print json.dumps(latest_news, ensure_ascii=False, indent=2)

        latest_news_ids = fetch.extract_news_ids(latest_news)
        date_str = fetch.extract_date_str(latest_news)

        for id in latest_news_ids:
            if News.objects.filter(news_id=id).exists():
                continue
            news = zh.get_news(id)
            image_name, image = fetch.fetch_image(news['share_url'], news['image'])
            news_obj, _ = News.objects.get_or_create(
                news_id=id,
                date=date_str,
                title=news['title'],
                share_url=news['share_url'],
                image_source=news['image_source']
            )
            news_obj.image.save(image_name, image)

    def cron_run(self):
        interval_hour = 2
        while True:
            try:
                self.insert_data()
            except:
                pass
            time.sleep(interval_hour * 3600)
