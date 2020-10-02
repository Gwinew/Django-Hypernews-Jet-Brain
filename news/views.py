import json
import datetime
import random

from itertools import groupby
from django.db.models import Q
from django.conf import settings
#from django.http import HttpResponse
from django.shortcuts import render, redirect


def read_json():
    with open(settings.NEWS_JSON_PATH) as f:
        news_list = json.load(f)
    return news_list


def save_json(data_dict):
    with open(settings.NEWS_JSON_PATH, 'w') as f:
        json.dump(data_dict, f)


def home(request):
    return redirect('/news')


def index(request):
    sorted_news = sorted(read_json(), key=lambda x: x['created'], reverse=True)
    grouped_by_date = {}
    for k, v in groupby(sorted_news, lambda x: x['created'][:10]):
        grouped_by_date[k] = list(v)
    query = request.GET.get('q')
    submitbutton = request.GET.get('submit')
    if query:
        list_of_title = {}
        for i, j in grouped_by_date.items():
            for e in j:
                if query in e['title']:
                    list_of_title[i] = list(j)
        return render(request, 'news/index.html', {'news': list_of_title})
    return render(request, 'news/index.html', {'news': grouped_by_date})




def detail(request, news_id):
    context = None
    for item in read_json():
        if news_id == item['link']:
            context = {'news': item}
    return render(request, 'news/detail.html', context)


def create(request):
    if request.method == 'GET':
        return render(request, 'news/create.html')
    if request.method == 'POST':
        news_list = read_json()
        used_links = [i['link'] for i in news_list]
        while True:
            link_id = random.randint(1, 65535)
            if link_id not in used_links:
                break
        news_list.append({
            'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': link_id,
        })
        save_json(news_list)
    return redirect('/news')
