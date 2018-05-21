from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Card, CardTemplate, PendingAction, \
    UtilisationStatus, TrendChangeDetectionPDecrease, TrendChangeDetectionPIncrease, BiogasSensorStatus, AutoFault, DataConnection, IndictorJoinTable
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from helpers import Permissions
from helpers import CustomBadRequest
from helpers import keep_fields
import uuid
import traceback
from copy import copy
from tastypie_actions.actions import actionurls, action
from django.core import serializers
import serpy
from django.db.models import Q
import uuid
import json
from helpers import datetime_to_string, error_handle_wrapper, only_keep_fields, map_fields, to_serializable, AddressSerializer, CardTemplateSerializer, CardSerializerNoPending, CardSerializerPending, raise_custom_error
from django.core.paginator import Paginator
from tastypie_actions.actions import actionurls, action
from django_postgres_extensions.models.functions import ArrayAppend, ArrayReplace
from django.contrib.gis.geos import Point
import datetime
import time
import pdb


class DataResource(ModelResource):
    class Meta:
        queryset = Card.objects.all() # everything in the Techicians database - or use Entry.objects.all().filter(pub_date__year=2006) to restrict what is returned
        resource_name = 'data' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post', 'put']
        filtering = {
                    } # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read", "write"),
            
        )

    def prepend_urls(self):
        return actionurls(self)


    def dehydrate(self, bundle):

        return bundle

    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_template_cards(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            part_of_companies = UserDetail.objects.get(user=uob).company.all()
            #logged_in_as = UserDetail.objects.get(user=uob).logged_in_as # use this in the future
            
            ##part_of_groups = uob.groups.all()
            ##perm = Permissions(part_of_groups)
            ##list_of_company_ids_admin = perm.check_auth_admin()
            ##list_of_company_ids_tech = perm.check_auth_tech()
            
            # use the commented out option below to filter by companies they are part of in the future - or better even filter by the comany they are logged in as
            #card_templates = CardTemplate.objects.filter(company__in = part_of_companies)
            # for now we just show all card tempates as there are not many and we want to display something for development purposes
            card_templates = CardTemplate.objects.all()
            card_templated_serialized = CardSerializerNoPending(card_templates, many=True).data
            
            bundle.data = { "data":card_templated_serialized }
        except:
            raise_custom_error({"error":"Cards not available at the moment"}, 500)

        return self.create_response(request, bundle)
        
        
        #pdb.set_trace()
        #data = json.loads( request.read() )
        #data = only_keep_fields(data,['technician'])
        
        # try:
        #     pk = int(kwargs['pk'])
        # except:
        #     pk = kwargs['pk']

    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_cards(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        #pdb.set_trace()
        try:
            uob = bundle.request.user
            part_of_companies = UserDetail.objects.get(user=uob).company.all()
            #logged_in_as = UserDetail.objects.get(user=uob).logged_in_as # use this in the future
            
            ##part_of_groups = uob.groups.all()
            ##perm = Permissions(part_of_groups)
            ##list_of_company_ids_admin = perm.check_auth_admin()
            ##list_of_company_ids_tech = perm.check_auth_tech()
            
            # use the commented out option below to filter by companies they are part of in the future - or better even filter by the comany they are logged in as
            #card_templates = CardTemplate.objects.filter(company__in = part_of_companies)
            # for now we just show all card tempates as there are not many and we want to display something for development purposes
            
            cards_with_pending_actions = Card.objects.filter(user=uob.userdetail).filter(pending_actions__isnull=False).filter(pending_actions__is_complete=False).all()
            cards_with_no_pending_actions = Card.objects.filter(user=uob.userdetail).filter(pending_actions__isnull=True)
            cards_no_pending_serialized = CardSerializerNoPending(cards_with_no_pending_actions, many=True).data
            cards_pending_serialized = CardSerializerPending(cards_with_pending_actions, many=True).data
            serialized = cards_pending_serialized + cards_no_pending_serialized
            bundle.data = { "data": serialized }
        except:
            raise_custom_error({"error":"Cards not available at the moment"}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False,static=True)
    def modify_card_order(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        data = only_keep_fields(data,['card_order'])
        try:
            uob = bundle.request.user
            part_of_companies = UserDetail.objects.get(user=uob).company.all()
            cards = Card.objects.filter(user=uob.userdetail)
            # check that the client does not try and put 2 cards in the same position
            positions_occupied = set()
            unique_check = any(pos in positions_occupied or positions_occupied.add(pos) for id_, pos in data['card_order'])
            if unique_check is True:
                raise_custom_error({"error":"You must a list with unique positions [[[id1,pos2],[id2,pos2]...etc]"}, 500)

            for id_, pos in data['card_order']:
                for cd in cards:
                    if (cd.id == id_):
                        cd.position = pos
                        cd.save(update_fields=['position'])
            bundle.data = { "message":"Card Positions updated" }
            # now update the correct cards       
        except:
            raise_custom_error({"error":"You cannot modify the order at this time"}, 500)

        return self.create_response(request, bundle)

    def pressure_data(self, request, **kwargs):
        self.is_authenticated(request)

    def get_latest_indictors(self, request, **kwargs): # for a particular biogas plant
        self.is_authenticated(request)
