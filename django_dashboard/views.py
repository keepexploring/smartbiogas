# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.core.serializers import serialize
from django_dashboard.models import AggregatedStatistics
import json
from dal import autocomplete
from django_dashboard.models import AddressData
from django.contrib.auth.models import User
#from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
import json
import pdb

# Create your views here.

#class RegionAutocomplete(autocomplete.Select2QuerySetView):
class RegionAutocomplete(autocomplete.Select2ListView):
    #serializer_class = serialize
    
    #def get_queryset(self):
    # def get(self, request):
    #     # Don't forget to filter out results depending on the visitor !
    #     if not self.request.user.is_authenticated():
    #         return AddressData.objects.none()

    #     #pdb.set_trace()
    #     qs = AddressData.objects.all().values('region','uid').distinct('region')
       

    #     if self.q:
    #         qs = qs.filter(region__istartswith=self.q)

    #     data = [{"text":ii["region"], "id":ii["uid"]} for ii in qs]
       
    #     return JsonResponse({"pagination":{"more":False}, "results":data})
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('region','uid').distinct('region')

        data = [ii["region"] for ii in qs]
        return data

class CountryAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('country','uid').distinct('country')

        data = [ii["country"] for ii in qs]
        return data

class ContinentAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('continent','uid').distinct('continent')

        data = [ii["continent"] for ii in qs]
        return data

class DistrictAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('district','uid').distinct('district')

        data = [ii["district"] for ii in qs]
        return data

class WardAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('ward','uid').distinct('ward')

        data = [ii["ward"] for ii in qs]
        return data

class VillageAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        qs = AddressData.objects.all().values('village','uid').distinct('village')

        data = [ii["village"] for ii in qs]
        return data

class SupplierAutocomplete(autocomplete.Select2ListView):
    suppliers = ['creativenergie', 'Camartec', 'Simgas', 'Biobalsa','Local technician']
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        return self. suppliers

class VolumeAutocomplete(autocomplete.Select2ListView):
    volume = ['<3m3','3m3','4m3','5m3','6m3','7m3','8m3','9m3','10m3','11m3','12m3','>12m3']
    def get_list(self):
        if not self.request.user.is_authenticated():
             return []
        return self.volume



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