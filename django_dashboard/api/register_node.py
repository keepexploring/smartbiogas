from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import RegisteredNode
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from helpers import Permissions
from django.db.models import Q
from tastypie.constants import ALL
from helpers import keep_fields
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from django_dashboard.api.api import TechnicianDetailResource, UserDetailResource
from tastypie_actions.actions import actionurls, action
from helpers import remove_fields, to_serializable, CustomBadRequest, only_keep_fields
from cerberus import Validator
from django.core import serializers
import uuid
import json
#from django_dashboard.api.api_biogas_contact import BiogasPlantContactResource
from django_dashboard.api.validators.validator_patterns import schema
from django.contrib.auth.models import Group
from django_dashboard.api.validators.validator_patterns import schema
from cerberus import Validator
import pdb

class RegisterResource(ModelResource):
    class Meta:
            queryset = RegisteredNode.objects.all() # everything in the Techicians database - or use Entry.objects.all().filter(pub_date__year=2006) to restrict what is returned
            resource_name = 'register' # when it is called its name will be called technicians
            excludes = []
            list_allowed_methods = ['get', 'post', 'put']
            filtering = {'UIC':ALL,
                        'channel':ALL,
                        'band':ALL,
                        'mode':ALL,
                        } # can use the filtering options from django
            authorization = DjangoAuthorization()
            authentication = OAuth2ScopedAuthentication(
                post=("read write",),
                get=("read",),
                put=("read", "write"),
                
            )

    def prepend_urls(self):
        return actionurls(self)

    
    @action(allowed=['post'], require_loggedin=False, static=True)
    def register_node(self, request, **kwargs):
        self.is_authenticated(request)

        bundle = self.build_bundle(data={}, request=request)     
        data = json.loads( request.read() )
        data = only_keep_fields( data,['UIC', 'channel','band','mode', 'nw_key'] )
        
        register_node_schema = schema['register_node']
        vv= Validator(register_node_schema)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )

        uob = bundle.request.user
        if (uob.has_perm('django_dashboard.can_register_node')):
            if ( RegisteredNode.objects.filter( UIC = data['UIC'] ).exists() is False ):
                new_node = RegisteredNode.objects.create(UIC=data['UIC'], channel=data['channel'], band=data['band'], mode=data['mode'], nw_key=data['nw_key'])
                bundle.data = { "message":"Node Created" }
            else:
                raise CustomBadRequest( code="error", message="Node already exists, try a new UIC" )

        else:
            raise CustomBadRequest( code="error", message="You don't have permission to create a node" )
        

        return self.create_response(request, bundle)