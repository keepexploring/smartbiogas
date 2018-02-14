from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from tastypie.constants import ALL
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from tastypie.bundle import Bundle
from helpers import CustomBadRequest
from helpers import keep_fields
import datetime
import pytz
import uuid
import traceback
import pdb

class Active(object):
    id = None
    active = None

d1 = Active()
d1.id = 1
d1.active = False

data = {1:d1}

class ValidateToken(Resource):
    id = fields.IntegerField(attribute = 'id')
    active = fields.BooleanField(default=False)
    
    class Meta:
        resource_name = 'validate'
        object_class = Active
        list_allowed_methods = ['get']
        authorization = Authorization()
        authentication = Authentication()
     
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        # inner get of object list... this is where you'll need to
        # fetch the data from what ever data source
        #pdb.set_trace()
        return data.values()

    def obj_get_list(self, request = None, **kwargs):
        # outer get of object list... this calls get_object_list and
        # could be a point at which additional filtering may be applied
        
        return self.get_object_list(request)

    def obj_get(self, request = None, **kwargs):
        # get one object from data source
        pk = int(kwargs['pk'])
        try:
            return data[pk]
        except KeyError:
            raise NotFound("Object not found") 

    def dehydrate(self, bundle):
        token = bundle.request.META["HTTP_TOKEN"]
        tok = OAuth2ScopedAuthentication().verify_access_token(token,bundle.request)
        valid = tok.is_valid()
        expires = tok.expires
        time_now = datetime.datetime.utcnow()
        time_now = time_now.replace(tzinfo=pytz.utc)
        time_remaining = expires - time_now
        bundle.data ={"active":True,"expires":time_remaining.seconds}
        return bundle

    
    # def obj_create(self, bundle, request = None, **kwargs):
    #     # create a new row
    #     #bundle.obj = Row()
    #     pdb.set_trace()
    #     # full_hydrate does the heavy lifting mapping the
    #     # POST-ed payload key/values to object attribute/values
    #     bundle = self.full_hydrate(bundle)
        
    #     # we add it to our in-memory data dict for fun
    #     #data[bundle.obj.id] = bundle.obj
    #     return bundle
    
    # def obj_update(self, bundle, request = None, **kwargs):
    #     # update an existing row
    #     pk = int(kwargs['pk'])
    #     try:
    #         bundle.obj = data[pk]
    #     except KeyError:
    #         raise NotFound("Object not found")
        
    #     # let full_hydrate do its work
    #     bundle = self.full_hydrate(bundle)
        
    #     # update existing row in data dict
    #     data[pk] = bundle.obj
    #     return bundle