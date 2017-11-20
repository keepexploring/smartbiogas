# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
    return render(request,"home2.html")


@login_required(login_url="login/")
def dashboard_main(request):
    return render(request,"dashboard_layout_example.html")
