#coding:utf-8
import os 
import sys
import urllib
import urllib2
import json
from main.models import Job
import re
import cookielib

class Spider(object):
    opener = None
    job_search_id = None
    smooth = True
    
    def __init__(self):
        self.get_opener(None)
    
    def get_opener(self, head):
        # deal with the Cookies
        if self.opener:
            return 
        cj = cookielib.CookieJar()
        pro = urllib2.HTTPCookieProcessor(cj)
        self.opener = urllib2.build_opener(pro)
#         header = []
#         for key, value in head.items():
#             elem = (key, value)
#             header.append(elem)
#         self.opener.addheaders = header
        
    def login(self):
#         url = 'https://ibmreferrals.com/ajax/action/login?uid=210&callback=jQuery18305450005878228694_1445430714662&action_this_page=%2F&action_next_page=%2F&email=zzbj%40cn.ibm.com&password=3a37db559ee6b41ad65ec8a697e77d7085cc3bc6&User.email=zzbj%40cn.ibm.com&User.usr_auth.password=*********&callback_success=loginSuccess&callback_error=loginError&callback_form_id=jPanelLoginForm&_=1445430910212'
        url = 'https://ibmreferrals.com/ajax/action/login'
        values = {
            'uid': '752',
            'callback': 'jQuery183001578835374675691_1445427644724',
            'action_this_page': '%2F',
            'action_next_page': '%2F',
            'email': 'zzbj@cn.ibm.com',
            'password': '3a37db559ee6b41ad65ec8a697e77d7085cc3bc6',
            'User.email': 'zzbj@cn.ibm.com',
            'User.usr_auth.password': '*********',
            'callback_success': 'loginSuccess',
            'callback_error': 'loginError',
            'callback_form_id': 'jPanelLoginForm',
            '_': '1445427666754'
        }
        data = urllib.urlencode(values)
        geturl = url + '?' + data
        op = self.opener.open(geturl)
        data = op.read()
        print(data.decode())
    
    def weave(self):
        self.login()
        self.smooth = True
        job_ids = []
        self.get_job_serach_id()
        raw = self.get_jobs(1)
        pattern = re.compile(r'<div id="jPaginateNumPages" class="ghost">([\d]+)')
        m = pattern.search(raw)
        if m:
            pages = int(m.group(1))
        print('pages:',pages)
        job_ids.extend(self.spy(raw))
        for i in range(2, pages+1):
            raw = self.get_jobs(i)
            job_ids.extend(self.spy(raw))
        if self.smooth:
            self.delete_redundancy(job_ids)
    
    def get_ref_link(self, id):
        values = {
            'Job.id': id,
        }
        data = urllib.urlencode(values).encode(encoding='UTF8')
        url = 'http://ibmreferrals.com/ajax/job_short_url?uid=662'
        request = urllib2.Request(url, data)
        response = self.opener.open(request)
        response_in_json = json.loads(response.read().decode())
        ref_link = None
        if response_in_json:
            if response_in_json.get("Status") == 'OK':
                if response_in_json.get("Result"):
                    ref_link = response_in_json.get("Result").get("job_short_url")
        if ref_link:
            return ref_link
        else:
            print('got empty ref link:', id)
            return self.get_ref_link(self, id)
    
    def delete_redundancy(self, job_ids):
        for job in Job.objects.all():
            if not job.id in job_ids:
                job.delete()
    
    def spy(self, raw):
#         print('spyin raw:', raw.encode('utf8'))
        pattern = re.compile(r'job_list_(\d+).*?<a href="(http://ibmreferrals.com/.*?)".*?>(.*?)<.*?class="location">(.*?)<.*?class="category">(.*?)<.*?class="jlr_description">(.*?)<', re.U)
        job_ids = []
        for m in pattern.finditer(raw):
            job_ids.append(int(m.group(1)))
            if not Job.objects.filter(id=m.group(1)):
                try:
                    description, bonus = self.handle_description(m.group(6))
                    Job.objects.create(
                        id = int(m.group(1)),
                        link = m.group(2),
                        name = m.group(3),
                        location = self.handle_location(m.group(4)),
                        category = m.group(5),
                        description = description,
                        bonus = bonus
                    )
                    print('got job:', m.group(1))
                except Exception as ie:
                    print(ie)
                    print(m.groups())
                    self.smooth = False
        return job_ids
    
    def handle_location(self, location_raw):
        return location_raw.replace(', China', '')
    
    def handle_description(self, description_raw):
        bonus_tip = 'IBM Employees may earn a referral bonus for a successful hire.'
        bonus = False
        if description_raw.find(bonus_tip) >= 0:
            bonus = True
        return (description_raw.replace(bonus_tip, '').replace('&bull;', '').replace('Job description', '').strip(), bonus) 
    
    def get_jobs(self, index):
        print('loading page:', index)
        try:
            values = {
                'JobSearch.id': self.job_search_id,
                'page_index': index,
                'site-name': 'default527',
                'include_site': 'true',
                'uid': 641,
            }
            data = urllib.urlencode(values)
            url = 'http://ibmreferrals.com/ajax/content/job_results'
            geturl = url + '?' + data
            request = urllib2.Request(geturl)
            response = self.opener.open(request)
            response_in_json = json.loads(response.read().decode('utf8'))
            if response_in_json:
                return response_in_json.get('Result').replace('\t', '').replace('\n', '')
            return None
        except Exception as e:
            print(e)
            print('try again')
            self.get_jobs(index)
    
    def get_job_serach_id(self):
        values = {
            'keywords':'',
            'geo_location':'China',
            'geo_lat':'29.873',
            'geo_long':'121.551',
            'geo_level':'country',
            'geo_area_id':'G_1814991',
            'geo_country_area_id':'G_1814991',
            'geo_search_radius_km':'80.50',
            'geo_search_radius_units':'mi',
            'geo_region_area_id':'G_1809935',
        }
        data = urllib.urlencode(values).encode(encoding='UTF8')
        url = 'http://ibmreferrals.com/ajax/jobs/search/create?uid=459'
        request = urllib2.Request(url, data)
        response = self.opener.open(request)
        response_in_json = json.loads(response.read().decode())
        if response_in_json:
            if response_in_json.get("Status") == 'OK':
                if response_in_json.get("Result"):
                    self.job_search_id = response_in_json.get("Result").get("JobSearch.id")
    

