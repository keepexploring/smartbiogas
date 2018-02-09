# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
import json
from dal import autocomplete
from django.contrib.auth.models import User
#from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
import json
import pdb


class AppView(View):
    template_name = 'app.html'
    #@method_decorator(login_required)
    def get(self,request):
        #pdb.set_trace()
        data={}
        return render(request,self.template_name) # {'data':json.dumps(data)}
