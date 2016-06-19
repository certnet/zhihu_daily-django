import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from crawl.fetch import today_str, yesterday_date_str, tomorrow_date_str

from .models import News
#  from utils.cache_util import cached


# Create your views here.

def index(request):
    date_str = request.GET.get("date", today_str())
    context = {}
    try:
        news_list = News.objects.filter(date=date_str)

        before_date = yesterday_date_str(date_str)
        after_date = tomorrow_date_str(date_str) \
            if today_str() != date_str else None

        context = {
            'news_list': news_list,
            'before_date': before_date,
            'after_date': after_date
        }
    except Exception as e:
        import traceback
        stack = traceback.format_exc()
        logging.error("get daily news failed date_str:%s error:%s cause:%s"
                      % (date_str, e, stack))
    else:
        return render(request, 'daily.html', context)


def search(request):
    page_size = 2
    keyword = request.GET.get('keyword', '')
    page = request.GET.get('page', 1)
    if not keyword.strip():
        return redirect('/daily/')

    try:
        news_list = News.objects.filter(title__contains=keyword)
        paginator = Paginator(news_list, page_size)
        page_range = paginator.page_range
        hits = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        hits = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        hits = paginator.page(paginator.num_pages)
    else:
        context = {
            'page': page,
            'page_range': page_range,
            'keyword': keyword,
            'hits': hits,
        }
        return render(request, 'search.html', context)
