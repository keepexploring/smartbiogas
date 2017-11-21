# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(login_required(login_url="login/"),name='get')
class HomeDashboard(View):
    template_name = 'home.html'

    def get(self,request):
        return render(request,self.template_name)

@login_required(login_url="login/")
def index_view(request):
    return render(request,"index.html")