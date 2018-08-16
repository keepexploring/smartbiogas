from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Card, CardTemplate, PendingAction, \
    UtilisationStatus, TrendChangeDetectionPDecrease, TrendChangeDetectionPIncrease, BiogasSensorStatus, AutoFault, DataConnection, IndictorJoinTable, UICtoDeviceID, IndicatorsTemplate, IndicatorObjects
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
from helpers import datetime_to_string, error_handle_wrapper, only_keep_fields,remove_fields_from_dict, map_fields, \
                    to_serializable, AddressSerializer, CardTemplateSerializer, CardSerializerNoPending, \
                    CardSerializerPending, TemplateCardSerializer,  raise_custom_error, get_enum_id, IndicatorObjectsSerialiser, \
                    Permissions, to_serializable_location
from django.core.paginator import Paginator
from tastypie_actions.actions import actionurls, action
from django_postgres_extensions.models.functions import ArrayAppend, ArrayReplace
#from django.contrib.gis.geos import Point
import datetime
import get_and_push_data
import time
import os
import ConfigParser
import json
import pycountry
from django_dashboard.api.file_uploadmixin.forms import UploadFileForm
from django_dashboard.api.file_uploadmixin.mixins import MultipartResource
from django_dashboard.api.file_uploadmixin.handlefileupload import handle_uploaded_file
from django_dashboard.enums import EntityTypes, AlertTypes
from helpers import validate_data
from django_dashboard.api.validators.validator_patterns import schema
from django.core.exceptions import ObjectDoesNotExist
import pdb

#BASE_DIR = os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir)+ os.sep + os.pardir)
#BASE_DIR = os.path.normpath(os.path.normpath(os.getcwd())

BASE_DIR = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ os.sep + os.pardir)

Config = ConfigParser.ConfigParser() # we store security setting in another file
Config.read(BASE_DIR+'/config/configs.ini')


with open(os.path.join(os.path.dirname(__file__), 'country_data.json'),'r') as data_file:    
    country_data = json.load(data_file)

class DataResource(MultipartResource, ModelResource):
    class Meta:
        queryset = Card.objects.all() # everything in the Techicians database - or use Entry.objects.all().filter(pub_date__year=2006) to restrict what is returned
        fields = ('title', 'body', 'image')
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
    def get_template_cards(self, request, **kwargs): # create a new method to get all template card and restrict this one to only return template cards for a given company (this is used by the frontend)
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
            card_templated_serialized = TemplateCardSerializer(card_templates, many=True).data
            
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

    @action(allowed=['post'], require_loggedin=False,static=True)
    def add_card_to_dashboard(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields( data,['position', 'template_id'] )
        
        try:
            uob = bundle.request.user
            cards = Card.objects.filter(user=uob.userdetail)
            currently_occupied_positions = []
            for card in cards:
                currently_occupied_positions.append(card.position)

            
            try:
                template = CardTemplate.objects.get(id = data['template_id'])
            except:
                raise LookupError('Could not find that id. Are you sure you have the card id correct?')
            
            
            if data['position'] not in currently_occupied_positions:
                new_card = Card()
                new_card.position = data['position']
                new_card.card_template = template
                new_card.user = uob.userdetail
                new_card.save()
                bundle.data = { "message":"Card Added", "position":data['position'], "id":data['template_id'] }
            else:
                raise ValueError('The position you have given is currently occupied')
        except Exception as err:
            raise_custom_error({"error":str(err.__str__())}, 400)
        
        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False,static=True)
    def remove_card_from_dashboard(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields( data,['card_id'] )

        uob = bundle.request.user
        cards = Card.objects.filter(id=data['card_id'])
        if (len(cards) >=1):
            cards.delete()
            bundle.data = { "message":"Card Deleted", "card_id":data['card_id'] }
        else:
            raise_custom_error({"error":" There is not a card of that id on the dashboard" }, 400)

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
            unique_check = any(item['position'] in positions_occupied or positions_occupied.add(item['position']) for item in data['card_order'])
            if unique_check is True:
                raise_custom_error({"error":"You must provide a list with unique positions e.g. { 'card_order':[{'position':1,'id':7}, 'position':2,'id':5}, ...]}"}, 400)
            for item in data['card_order']:
                
                id_ = item['id']
                pos = item['position']

                for cd in cards:
                    if (cd.id == id_):
                        cd.position = pos
                        cd.save(update_fields=['position'])
            bundle.data = { "message":"Card Positions updated" }
            # now update the correct cards       
        except:
            raise_custom_error({"error":"You cannot modify the order at this time - You must provide a list with unique positions [[[id1,pos2],[id2,pos2]...etc]"}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def pressure_data(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields(data,['startT', 'endT', 'UIC','plant_id'])
        
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
                if 'UIC' in data:
                    device_id = UICtoDeviceID.objects.filter(biogas_plant__UIC=data['UIC'])[0].device_id
                elif 'plant_id' in data:
                    device_id = UICtoDeviceID.objects.filter(biogas_plant__id=data['device_id'])[0].device_id
            except:
                device_id = '1e7e59ddc13c9c09e6a33a31860bc0d' # hardcode now for testing
            sensor_data = next(data_to_get.get_data_for_device(device_id = device_id, name='', startT = 1513987200000, endT = 1514160000000))
            if 'UIC' in data:
                bundle.data = { "data":sensor_data , "UIC": data["UIC"] }
            elif 'plant_id' in data:
                bundle.data = { "data":sensor_data , "plant_id": data["plant_id"] }
        except:
            raise_custom_error({"error":"You cannot get pressure data at this time or there is an error with your request. Sorry not to be more helpful. Goodbye."}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def upload_photo(self, request, **kwargs):
        self.is_authenticated(request)

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],file_type)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def get_latest_indictors(self, request, **kwargs): # for a particular biogas plant
        """Returns the lastest indictors for a given biogas plant"""
        self.is_authenticated(request)
        
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        data = json.loads( request.read() )
        data = only_keep_fields(data,['plant_id'])
        try:
            perm = Permissions(uob)

            #part_of_companies = UserDetail.objects.get(user=uob).company.all()
            #indicators = IndictorJoinTable.objects.filter( plant__id = data['plant_id'] )
            indicators = IndicatorObjects.objects.filter(biogas_plant__id = data['plant_id'])
            
            # indicator_objects = {
            #     "utilisation": indicator.utilisation.all().first(),
            #     "low_gas_pressure": indicator.low_gas_pressure.all().first(),
            #     "trend_change_detection_pdecrease": indicator.trend_detection_p_decrease.all().first(),
            #     "trend_change_detection_pincrease": indicator.trend_detection_p_increase.all().first(),
            #     "biogas_sensor_status": indicator.biogas_sensor_status.all().first(),
            #     "autofault": indicator.auto_fault.all().first(),
            #     "data_connection": indicator.data_connection.all().first()
            # }
            # indictor_dict = {}
            # for i_key in indicator_objects.keys():
            #     try:
            #         indictor_dict[i_key] = { "status":indicator_objects[i_key].status , "info":indicator_objects[i_key].info, "created":indicator_objects[i_key].created.strftime("%Y-%m-%dT%H:%M:%S") }
            #     except:
            #         pass
            indictor_dict = IndicatorObjectsSerialiser(indicators, many=True).data
            bundle.data = { "data":indictor_dict , "plant_id": data["plant_id"] }
                   
        except:
            raise_custom_error({"error":"Your request has not succeeded. Sorry not to be more helpful. Goodbye."}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def update_card_value(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        if uob.is_superuser:
            data = json.loads( request.read() )
            data = only_keep_fields(data,['template_id', 'value'])
            validate_data(schema['update_card_value'],data)
            try:
                uuid_template_id = uuid.UUID(data['template_id'])
                template_cards = CardTemplate.objects.get( template_id=uuid_template_id )
                cards = template_cards.cards
                cards.update(value = data['value']) # need to update all the cards returned - check this
                bundle.data = { "value":data['value'] , "template_id": data['template_id'],"result":"updated" }
            except:
                raise_custom_error({"error":"template with that template_id cannot be found" }, 400)
                
        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def update_or_add_pending_action_for_a_template(self, request, **kwargs): # we could also have an action that updates the pending action for an individual card - if that was necessary e.g. to send a message to an individual user
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        
        if uob.is_superuser:
            data = json.loads( request.read() )
            data = only_keep_fields(data,['template_id','message','alert_type','entity_id','action_url','action_object'])
            validate_data(schema['update_or_add_pending_action'],data)
            
            try:
                uuid_template_id = uuid.UUID(data['template_id'])
                template_card = CardTemplate.objects.get( template_id=uuid_template_id )
            except:
                raise_custom_error({"error":"template with that template_id cannot be found" }, 400)
            try:
                
                entity_type = template_card.entity_type
                entity_type = entity_type.value
                cards = template_card.cards
                alert_type = get_enum_id(AlertTypes,data['alert_type'])
                
                pending_act = {"is_complete":False, "entity_type":entity_type, "alert_type":alert_type}
                data = remove_fields_from_dict(data,['alert_type','entity_type','template_id'])
            
                for item in data:
                    if item is 'entity_id':
                        try:
                            pending_act[item] = int(data[item])
                        except:
                            pass
                    else:
                         pending_act[item] = data[item]

                for card in cards.all():
                    #pending_actions = card.pending_actions
                    pending_act["card"] = card
                    pendingaction = PendingAction(**pending_act)
                    pendingaction.save()
            except:
                raise_custom_error({"error":"There are no cards yet associated with this template" }, 400)
                
        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def update_indicators(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        
        if uob.is_superuser:
            data = json.loads( request.read() )
            data = only_keep_fields(data,['plant_id','type_indicator','info','status','value'])
            validate_data(schema['update_indicators'],data)

            try:
                template_obj = IndicatorsTemplate.objects.get( type_indicator=data['type_indicator'] )
            except ObjectDoesNotExist:
                indicator_options = [ii.type_indicator for ii in IndicatorsTemplate.objects.all()]
                raise_custom_error({"error":"There are no Indicators of that type available. The options are: " + str(indicator_options) }, 400)
            
            try:
                plant_id = data['plant_id']
                indicator = IndicatorObjects.objects.get(biogas_plant__id = plant_id,indicator_template__type_indicator=data['type_indicator'])
            except:
                try:
                    biogas_plant_obj = BiogasPlant.objects.get(id=plant_id)
                    indicator=IndicatorObjects(biogas_plant=biogas_plant_obj, indicator_template = template_obj)
                except:
                    raise_custom_error({"error":"A biogas plant of that id does not exist" }, 400)

            try:

                data = remove_fields_from_dict(data,['plant_id', 'type_indicator'])
                for item in data:
                    setattr(indicator, item, data[item])
                indicator.save()
                bundle.data = { "plant_id":plant_id, "status":"success" }
            except:
                raise_custom_error({"error":"Problem updating indicator" }, 500)

        return self.create_response(request, bundle)




#login_body= {'username': 'smartbiogas', 'password': 'fGCEp9ZqEW5tsmYsRAGQiLD267Ae'}
#login_url = 'http://localhost:8000/token_generation'
#login_headers = {'Content-Type': 'application/json'}
# rr = requests.post(login_url,data=json.dumps(login_body), headers=login_headers)