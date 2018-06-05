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
from helpers import only_keep_fields, if_empty_fill_none, Permissions, map_fields, to_serializable
from tastypie_actions.actions import actionurls, action
import json

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

    def prepend_urls(self):
        return actionurls(self)

    
    
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

    @action(allowed=['post'], require_loggedin=False, static=True)
    def create_biogas_contact(self, request, **kwargs):
        
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["contact_type", "firstname", "surname","mobile","country","village","region","district","ward","latitude","longitude","what3words","UIC"]
        data = only_keep_fields(data, fields)
        data = if_empty_fill_none(data, fields)
        #pdb.set_trace()
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()

            contact = BiogasPlantContact() # if plant_id is a field we need to add it to the plant that has been specified
            contact.first_name = data['firstname']
            contact.surname = data['surname']
            contact.mobile = data['mobile']
            contact.contact_type = data['contact_type']
            contact.region = data['region']
            contact.district = data['district']
            contact.ward = data['ward']
            contact.village = data['village']
            bb=contact.save()
            try:
                if "latitude" in data.keys() and "longitude" in data.keys():
                    contact.update(lat_long=Point(data['longitude'],data['latitude']) )
            except:
                pass

            uuid = contact.uid

            #create(first_name=data['firstname'],surname=surname,mobile,contact_type=contact_type, mobile=mobile, email=email)
            bundle.data = {"message":"contact created","uid":uuid.hex}
        except:
             bundle.data = {"message":"error"}

        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False, static=True)
    def find_biogas_owner(self, request, **kwargs):
        #pdb.set_trace()
        self.is_authenticated(request)
        
        data = json.loads( request.read() )
        data = only_keep_fields(data, ["mobile"] )
        
        try:
            bundle = self.build_bundle(data={}, request=request)
            uob = bundle.request.user
            if uob.is_superuser:
                part_of_groups = uob.groups.all()
                perm = Permissions(part_of_groups)
                list_of_company_ids_admin = perm.check_auth_admin()
                list_of_company_ids_tech = perm.check_auth_tech()
                #pdb.set_trace()
                contacts = BiogasPlantContact.objects.filter(mobile=data['mobile'])
                data_to_return = []
                for cc in contacts:
                    biogas_owner = {}
                    biogas_owner['first_name'] = cc.first_name
                    biogas_owner['mobile'] = cc.mobile
                    biogas_owner['first_name'] = cc.first_name
                    biogas_owner['contact_type'] = cc.contact_type.name
                    biogas_owner['email'] = cc.email
                    biogas_owner['contact'] = to_serializable(cc.uid)[0]
                    biogas_owner['location'] = to_serializable(cc.lat_long)
                    biogas_owner['village'] = cc.village
                    biogas_owner['ward'] = cc.ward
                    biogas_owner['region'] = cc.region
                    biogas_owner['district'] = cc.district
                    biogas_owner['country'] = cc.country
                    biogas_plant_queryset = cc.biogas_plant_detail.get_queryset()
                    biogas_plants_owned_list = []
                    #pdb.set_trace()
                    for bb in biogas_plant_queryset:
                        biogas_plant_owned = {}
                        biogas_plant_owned['UIC'] = to_serializable(bb.UIC)[0]
                        biogas_plant_owned['biogas_plant_name'] = to_serializable(bb.biogas_plant_name)[0]
                        biogas_plant_owned['country'] = to_serializable(bb.country)[0]
                        biogas_plant_owned['region'] = to_serializable(bb.region)[0]
                        biogas_plant_owned['district'] = to_serializable(bb.district)[0]
                        biogas_plant_owned['ward'] = to_serializable(bb.ward)[0]
                        biogas_plant_owned['village'] = to_serializable(bb.village)[0]
                        biogas_plant_owned['other_address_details'] = to_serializable(bb.other_address_details)[0]
                        biogas_plant_owned['type_biogas'] = to_serializable(bb.type_biogas)[0]
                        biogas_plant_owned['supplier'] = to_serializable(bb.supplier)[0]
                        biogas_plant_owned['volume_biogas'] = to_serializable(bb.volume_biogas)[0]
                        biogas_plant_owned['location']=to_serializable(cc.lat_long)
                        # biogas_plant_owned['latitude'] = to_serializable(bb.location)[1]
                        # biogas_plant_owned['longitude'] = to_serializable(bb.location)[0]
                        biogas_plant_owned['sensor_status'] = to_serializable(bb.sensor_status)[0]
                        biogas_plant_owned['current_status'] = to_serializable(bb.current_status)[0]
                        biogas_plant_owned['verfied'] = to_serializable(bb.verfied)[0]
                        biogas_plant_owned['install_date'] = to_serializable(bb.install_date)[0]
                        biogas_plants_owned_list.append(biogas_plant_owned)
                    #pdb.set_trace()
                    biogas_owner['biogas_plants'] = biogas_plants_owned_list
                    data_to_return.append(biogas_owner)
                bundle.data['data'] = data_to_return
            else:
                bundle.data = {"message":"you are not authorised"}
        except Exception as e:
            print(e)

        return self.create_response(request, bundle)

    @action(allowed=['delete'], require_loggedin=False, static=False)
    def remove_owner_from_database():
        self.is_authenticated(request)
        data = json.loads( request.read() )
        data = only_keep_fields(data, ["id"])
        bundle = self.build_bundle(data={}, request=request)
        try:
            pass
        except:
            pass
        
        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=False)
    def create_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        data = only_keep_fields(data, ["firstname", "surname","mobile","owner","village","region","district","wards","what3words"])
        bundle = self.build_bundle(data={}, request=request)
        try:
            uid = uuid.UUID(hex=pk)
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            contact = BiogasPlantContact.objects.create(first_name,surname,mobile,contact_type)

        except:
            pass

        return self.create_response(request, bundle)


    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        
        if uob.is_superuser:
            pass

        else:
            bundle.data = {}

        return super(BiogasPlantContactResource, self).obj_create(bundle, user=bundle.request.user)
        
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