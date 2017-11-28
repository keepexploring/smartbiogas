
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

# Create your views here.


class index_main(View):
    template_name = 'index.html'
    @method_decorator(login_required)
    def get(self,request):
        return render(request,self.template_name)


@login_required()
def index_home(request):
    template_name = 'index.html'
    return render(request,template_name)