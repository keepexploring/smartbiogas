from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from django.db.models import Q

import pdb


class BiogasPlantContactResource(ModelResource):
    biogas_plant_details = fields.ManyToManyField(BiogasPlantResource, 'biogas_plant_detail',null=True, blank=True, full=True)

    class Meta:
        queryset = BiogasPlantContact.objects.all()
        resource_name = 'biogasplantcontacts'
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = { "title":ALL , "mobile":ALL }
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
    
    def obj_update(self, bundle, **kwargs):
        #pdb.set_trace()
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        uob = bundle.request.user
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)
        list_of_company_ids_admin = perm.check_auth_admin()
        list_of_company_ids_tech = perm.check_auth_tech()

        if uob.is_superuser:
            try:
                bundle.obj = BiogasPlantContact.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True:
                try:
                    bundle.obj = BiogasPlantContact.objects.get( pk=pk,associated_company__company_id__in = list_of_company_ids_admin[1] ) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['contact_type','first_name','surname','mobile','email','associated_company']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and list_of_company_ids_tech[0] is True ):
                try:
                    bundle.obj = BiogasPlantContact.objects.get( pk=pk,associated_company__company_id__in = list_of_company_ids_admin[1])
                    #bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_tech[1]) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['contact_type','first_name','surname','mobile','email','associated_company']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="You do not have permission to edit that contact")
                
            else:
                bundle.obj = BiogasPlantContact.objects.none()
                bundle.data ={}

        bundle = self.full_hydrate(bundle)

        #pdb.set_trace(0)
        return super(BiogasPlantContact, self).obj_update(bundle, user=uob)

    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)

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
            return object_list.filter(associated_company__company_name__in=company_names)

        if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            return []