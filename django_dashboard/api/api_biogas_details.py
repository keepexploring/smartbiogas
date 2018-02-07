from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL
#from django_dashboard.api.api_biogas_contact import BiogasPlantContactResource

import pdb


class BiogasPlantResource(ModelResource):

    #contact = fields.ToManyField(BiogasPlantContactResource, 'contact',null=True, blank=True, full=True)

    #contact = fields.ManyToManyField(BiogasPlantContactResource)
    class Meta:
        queryset = BiogasPlant.objects.all()
        resource_name = 'biogasplants'
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = {'funding_souce':ALL,
                    'supplier':ALL,
                    'QP_status':ALL,
                    'current_status':ALL,
                    'funding_souce':ALL,
                    'sensor_status':ALL,
                    'volume_biogas':ALL,
                    'type_biogas':ALL,
                    'size_biogas':ALL,
                    'country':ALL,
                    'region':ALL,
                    'district':ALL,
                    'ward':ALL,
                    'village':ALL,
                    
                    }
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )

    def dehydrate(self, bundle):
        #pdb.set_trace()
        dat = bundle.obj.contact.values()
        bundle.data['contact'] = [i for i in dat]
        return bundle

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        if uob.is_superuser:
            return object_list

        if user_object[0].role.label == 'Company Admin': # return all the people associated with this company
            #pdb.set_trace()
            company_object = user_object[0].company.all()
            company_names = [co.company_name for co in company_object]
            return object_list.filter(contact__associated_company__company_name__in=company_names)

        if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            #pdb.set_trace()
            # we want to filter and return only the biogas plants associated with that technican
            #object_list.biogas_plant_detail
            return []