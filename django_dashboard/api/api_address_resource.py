from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, AddressData, AddressLocation
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.paginator import Paginator
from helpers import Permissions, only_keep_fields, if_empty_fill_none, to_serializable, to_serializable_location, raise_custom_error, BiogasPlantSerialiser
from django.db.models import Q
from tastypie.constants import ALL
from tastypie_actions.actions import actionurls, action
#from django.contrib.gis.geos import Point
from django.core import serializers
from helpers import AddressSerializer, CustomBadRequest
from cerberus import Validator
import serpy
import uuid
import json
from django.db import transaction
#from django_dashboard.api.api_biogas_contact import BiogasPlantContactResource
from django_dashboard.api.validators.validator_patterns import schema
from django_dashboard.api.addressmapper import get_address_keywords, create_address_object, map_database_to_address_object, map_address_to_database, map_address_to_json_from_database, map_serialised_address
import pdb



class AddressResource(ModelResource):

    #contact = fields.ToManyField(BiogasPlantContactResource, 'contact',null=True, blank=True, full=True)

    #contact = fields.ManyToManyField(BiogasPlantContactResource)
    class Meta:
        queryset = AddressLocation.objects.all()
        resource_name = 'biogasplants'
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = {'building_name_number':ALL,
                    'address_line1':ALL,
                    'address_line2':ALL,
                    'address_line3':ALL,
                    'region':ALL,
                    'city':ALL,
                    'zip_code':ALL,
                    'country':ALL,
                    'continent':ALL,
                    'other':ALL,
                    'what3words':ALL,
                    'latitude':ALL,
                    'longitude':ALL,
                    'srid':ALL,
                    }
                    
        ordering = ['funding_souce','supplier','QP_status','current_status','funding_souce','sensor_status','volume_biogas','type_biogas','size_biogas','country','region','district','ward','village','other_address_details','verfied','install_date']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            get=("read",),
        )
        paginator_class = Paginator

    def prepend_urls(self):
        return actionurls(self)

    def dehydrate(self, bundle):
        #pdb.set_trace()
        dat = bundle.obj.contact.values()
        bundle.data['contact'] = [i for i in dat]
        return bundle

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()
        user_object = UserDetail.objects.filter(user=uob)
        if ( uob.is_superuser or perm.is_global_admin() ):
            return object_list

        if perm.is_admin(): # return all the people associated with this company
            #pdb.set_trace()
            #company_object = user_object[0].company.all()
            #company_names = [co.company_name for co in company_object]
            #return object_list.filter(Q(contact__associated_company__company_name__in=company_names) | Q(associated_company__company_name__in=company_names))
            return object_list.filter( associated_company = company )

        if perm.is_technician(): # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            #pdb.set_trace()
            # we want to filter and return only the biogas plants associated with that technican
            #object_list.biogas_plant_detail
            return []

    def authorized_read_detail(self, object_list, bundle):
        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()
        user_object = UserDetail.objects.filter(user=uob)
        if ( uob.is_superuser or perm.is_global_admin() ):
            return object_list

        if perm.is_admin(): # return all the people associated with this company
            #pdb.set_trace()
            #company_object = user_object[0].company.all()
            #company_names = [co.company_name for co in company_object]
            #return object_list.filter(Q(contact__associated_company__company_name__in=company_names) | Q(associated_company__company_name__in=company_names))
            return object_list.filter( associated_company = company )

        if perm.is_technician(): # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            #pdb.set_trace()
            # we want to filter and return only the biogas plants associated with that technican
            #object_list.biogas_plant_detail
            return []