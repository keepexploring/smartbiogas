from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Card, CardTemplate, PendingAction, \
    UtilisationStatus, TrendChangeDetectionPDecrease, TrendChangeDetectionPIncrease, BiogasSensorStatus, AutoFault, DataConnection, IndictorJoinTable, UICtoDeviceID
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
import get_and_push_data
import time
import os
import ConfigParser
import json
import pycountry
import pdb

#BASE_DIR = os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir)+ os.sep + os.pardir)
#BASE_DIR = os.path.normpath(os.path.normpath(os.getcwd())

BASE_DIR = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ os.sep + os.pardir)

Config = ConfigParser.ConfigParser() # we store security setting in another file
Config.read(BASE_DIR+'/config/configs.ini')


with open(os.path.join(os.path.dirname(__file__), 'country_data.json'),'r') as data_file:    
    country_data = json.load(data_file)

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
    def get_countries_and_mobile_shortcodes(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        #pdb.set_trace()
        try:
            list_of_countries = list(pycountry.countries)

            countries_and_shortcodes = [{ "name":ii.name, "alpha_2":ii.alpha_2, "alpha_3":ii.alpha_3, "calling_code":country_data[ii.alpha_2]["callingCode"], "languages":[{"code":key,"name":value } for key,value in country_data[ii.alpha_2]["languages"].items()], "latlong" :country_data[ii.alpha_2]["latlng"]} for ii in list_of_countries]
            bundle.data = {"data": countries_and_shortcodes }
        except:
            raise_custom_error({"error":"Countries not available at the moment"}, 500)

        return self.create_response(request, bundle)


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

    @action(allowed=['post'], require_loggedin=False,static=True)
    def pressure_data(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields(data,['startT', 'endT', 'UIC'])
        
        try:
            uob = bundle.request.user
            part_of_companies = UserDetail.objects.get(user=uob).company.all()

            username = Config.get("thingsboardapi","username_set")
            password = Config.get("thingsboardapi","password_set")
            data_to_get = get_and_push_data.get_push_data(username=username, password=password)
            username = None # don't keep credentials stored in memory
            password = None
            # we would now need to look up the device_id on thingsboard from the UIC (that is the number on the hardware)
            
            try:
                device_id = UICtoDeviceID.objects.filter(UIC=data['UIC'])[0].device_id
            except:
                device_id = '1e7e59ddc13c9c09e6a33a31860bc0d' # hardcode now for testing
            sensor_data = next(data_to_get.get_data_for_device(device_id = device_id, name='', startT = 1513987200000, endT = 1514160000000))
            bundle.data = { "data":sensor_data , "UIC": data["UIC"] }
        except:
            raise_custom_error({"error":"You cannot get pressure data at this time or there is an error with your request. Sorry not to be more helpful. Goodbye."}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def get_latest_indictors(self, request, **kwargs): # for a particular biogas plant
        """Returns the lastest indictors for a given biogas plant"""
        self.is_authenticated(request)
        
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields(data,['plant_id'])
        try:
            uob = bundle.request.user
            part_of_companies = UserDetail.objects.get(user=uob).company.all()
            #indicators = IndictorJoinTable.objects.filter( plant__id = data['plant_id'] )
            indicators = IndictorJoinTable.objects.all() # initially as we don't have this part working yet
            indicator = indicators.first()
            indicator_objects = {
                "utilisation": indicator.utilisation.all().first(),
                "low_gas_pressure": indicator.low_gas_pressure.all().first(),
                "trend_change_detection_pdecrease": indicator.trend_detection_p_decrease.all().first(),
                "trend_change_detection_pincrease": indicator.trend_detection_p_increase.all().first(),
                "biogas_sensor_status": indicator.biogas_sensor_status.all().first(),
                "autofault": indicator.auto_fault.all().first(),
                "data_connection": indicator.data_connection.all().first()
            }
            indictor_dict = {}
            for i_key in indicator_objects.keys():
                try:
                    indictor_dict[i_key] = { "status":indicator_objects[i_key].status , "info":indicator_objects[i_key].info, "created":indicator_objects[i_key].created.strftime("%Y-%m-%dT%H:%M:%S") }
                except:
                    pass
            bundle.data = { "data":indictor_dict , "plant_id": data["plant_id"] }
                   
        except:
            raise_custom_error({"error":"Your request has not succeeded. Sorry not to be more helpful. Goodbye."}, 500)

        return self.create_response(request, bundle)


#login_body= {'username': 'smartbiogas', 'password': 'fGCEp9ZqEW5tsmYsRAGQiLD267Ae'}
#login_url = 'http://localhost:8000/token_generation'
#login_headers = {'Content-Type': 'application/json'}
# rr = requests.post(login_url,data=json.dumps(login_body), headers=login_headers)