
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django_dashboard.models import AggregatedStatistics
import json
import pdb

# Create your views here.


class index_main(View):
    template_name = 'index.html'
    @method_decorator(login_required)
    def get(self,request):
        #pdb.set_trace()
        data = AggregatedStatistics().get_data()
        return render(request,self.template_name,{'data':json.dumps(data)})


class Technicians(View):
    template_name = 'technicians.html'
    @method_decorator(login_required)
    def get(self,request):
        return render(request,self.template_name)


class Jobs(View):
    template_name = 'jobs.html'
    @method_decorator(login_required)
    def get(self,request):
       # pdb.set_trace()
        return render(request,self.template_name)

class Plants(View):
    template_name = 'plants.html'
    @method_decorator(login_required)
    def get(self,request):
        #pdb.set_trace()
        return render(request,self.template_name)


@login_required()
def index_home(request):
    template_name = 'index.html'
    return render(request,template_name)

@login_required()
def plants_test(request):
    template_name = 'plants.html'
    return render(request,template_name)