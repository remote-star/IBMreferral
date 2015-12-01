#coding:utf-8
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.core import serializers

from main.models import Job
from django.db.models import Q

import json


def index(request):  
    return render_to_response(
        'index.html',
        {'page' : 'index'},
        context_instance=RequestContext(request)
    )

def hot(request, tab='hot'):
    tabs = ('hot', 'openpower', 'gts', 'cio', 'sales', 'gbs', 'digital_sales')
    if tab in tabs:
        return render_to_response(
            'hot/' + tab + '.html',
            {'page' : 'hot',
             'sub' : tab},
            context_instance=RequestContext(request)
        )

def help(request, tab='tutorial'):
    tabs = ('tutorial', 'openpower', 'about_ibm', 'faq', 'contact')
    if tab in tabs:
        return render_to_response(
            'help/' + tab + '.html',
            {'page' : 'help',
             'sub' : tab},
            context_instance=RequestContext(request)
        )

def market(request, tab='market'):
    tabs = ('market', 'total')
    if tab in tabs:
        return render_to_response(
            'market/' + tab + '.html',
            {'page' : 'market',
             'sub' : tab},
            context_instance=RequestContext(request)
        )

def find_jobs(request):
    query = request.POST
    jobs = query_jobs(query)
    return HttpResponse(json.dumps(serializers.serialize("json", jobs)))

def query_jobs(query):
    jobs = Job.objects.all()
    if query.get('location') and query['location'] != '':
        jobs = jobs.filter(location = query['location'])
    if query.get('category') and query['category'] != '':
        jobs = jobs.filter(category = query['category'])
    if query.get('keyword') and query['keyword'] != '':
        jobs = jobs.filter(Q(name__contains = query['keyword']) | 
                           Q(location__contains = query['keyword']) |
                           Q(category__contains = query['keyword']) |
                           Q(description__contains = query['keyword']) )
    return jobs

# def get_other_menus(request):
#     other_menus = {}
#     selected_menu = request.POST['menu']
#     selected_item = request.POST['item']
#     query = {selected_menu : selected_item}
#     jobs = query_jobs(query)
#     
#     if selected_menu != 'location':
#         other_menus['location'] = [value['location'] for value in jobs.values('location').distinct()]
#     if selected_menu != 'category':
#         other_menus['category'] = [value['category'] for value in jobs.values('category').distinct()]
#     return HttpResponse(json.dumps(other_menus))

# def get_page_links(prefix, amount, current):
#     pagination = {}
#     pages = []
#     page_num = int((amount-1)/10)+1
#     begin = 1
#     end = page_num+1
#     
#     def _get_segment(begin, end):
#         pages = []
#         for i in range(begin, end):
#             page_link = {
#                 'num' : i,
#                 'link' : prefix + str(i),         
#             }
#             pages.append(page_link)
#         return pages
#     
#     if amount < 10:
#         return None
#     if amount > 90:
#         if current <= 5:
#             end = 10
#             pages.extend(_get_segment(begin, end))
#             pages.append({
#                 'num' : '..',
#                 'link' : prefix + str(current+1),         
#             })
#             pagination['next'] = prefix + str(current+1)
#         elif current > page_num-5:
#             begin = page_num-8
#             pages.append({
#                 'num' : '..',
#                 'link' : prefix + str(current-1),         
#             })
#             pages.extend(_get_segment(begin, end))
#             pagination['previous'] = prefix + str(current-1)
#         else:
#             begin = current-4
#             end = current+5
#             pages.append({
#                 'num' : '..',
#                 'link' : prefix + str(current-1),         
#             })
#             pages.extend(_get_segment(begin, end))
#             pages.append({
#                 'num' : '..',
#                 'link' : prefix + str(current+1),         
#             })
#             pagination['previous'] = prefix + str(current-1)
#             pagination['next'] = prefix + str(current+1)
#     else:
#         pages = _get_segment(begin, end)
#         
#     pagination['pages'] = pages
#     pagination['current'] = current
#     return pagination

def get_locations(request):
    locations =  [value['location'] for value in Job.objects.values('location').distinct()]
    return HttpResponse(json.dumps(locations))

def get_categories(request):
    categories =  [value['category'] for value in Job.objects.values('category').distinct()]
    return HttpResponse(json.dumps(categories))