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
    tabs = ('hot', 'openpower', 'gts', 'cio', 'sales', 'gbs', 'rnd', 'snd', 'gie')
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

def get_locations(request):
    locations =  [value['location'] for value in Job.objects.values('location').distinct()]
    return HttpResponse(json.dumps(locations))

def get_categories(request):
    categories =  [value['category'] for value in Job.objects.values('category').distinct()]
    return HttpResponse(json.dumps(categories))