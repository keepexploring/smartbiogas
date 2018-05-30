from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, AddressData
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from helpers import Permissions, only_keep_fields, if_empty_fill_none, to_serializable, raise_custom_error
from django.db.models import Q
from tastypie.constants import ALL
from tastypie_actions.actions import actionurls, action
from django.contrib.gis.geos import Point
from django.core import serializers
from helpers import AddressSerializer
import serpy
import uuid
import json
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

    def prepend_urls(self):
        return actionurls(self)


    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_wards_villages(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        bundle = self.build_bundle(data={}, request=request)
        address_data = AddressData.objects.all()
        addresses= AddressSerializer(address_data, many=True).data
        bundle.data = { 'data':addresses }

        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False,static=True)
    def get_biogas_plants(self, request, **kwargs):
        """Gte the biogas plants of an owner form their mobile number"""
        self.is_authenticated(request)
        data = json.loads( request.read() )
        mobile=data['mobile']
        bundle = self.build_bundle(data={}, request=request)
        try:
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            if uob.is_superuser:
                part_of_groups = uob.groups.all()
                perm = Permissions(part_of_groups)
                list_of_company_ids_admin = perm.check_auth_admin()
                list_of_company_ids_tech = perm.check_auth_tech
                #bundle.data['technicians'] = data_list
                biogas_plants = BiogasPlant.objects.filter(contact__mobile=mobile)
                #bundle.data['biogas_plants'] = [i for i in biogas_plants]

                data_list = []
                for bi in biogas_plants:
                    data = { 
                            "owner": [{"first_name":ii.first_name, "surname":ii.surname, "mobile":ii.mobile, "contact_type":ii.contact_type.name} for ii in bi.contact.all()],
                            "biogas_plant_name": bi.biogas_plant_name,
                             "associated_company": bi.associated_company,
                            "country":bi.country,
                            "region": bi.region,
                            "district":bi.district,
                            "ward": bi.ward,
                            "village":bi.village,
                            "type_biogas":bi.type_biogas,
                            "supplier":bi.supplier,
                            "volume_biogas":bi.volume_biogas,
                            "QP_status":bi.QP_status,
                            "sensor_status":bi.sensor_status,
                            "current_status":bi.current_status,
                            "verfied":bi.verfied,
                            "uri":"/api/v1/biogasplant/"+str(bi.id)+"/",
                            "location_estimated":bi.location_estimated,
                            "location": to_serializable(bi.location),
                           }
                    data_list.append(data)
                bundle.data['biogas_plants'] = data_list
        except:
            pass

        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False, static=True)
    def create_biogas_plant(self, request, **kwargs):
        
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["UIC", "biogas_plant_name", "associated_company","contact","funding_source","latitude","longitude","country","village","region","district","ward","what3words","type_biogas","volume_biogas","install_date","other_address_details","current_status","contruction_tech","location_estimated"]
        data = only_keep_fields(data, fields)
        data = if_empty_fill_none(data, fields)
        fields = data.keys()
        
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            biogasplant = BiogasPlant() # if plant_id is a field we need to add it to the plant that has been specified
            field_relations = {'UIC': biogasplant.UIC, 'biogas_plant_name':biogasplant.biogas_plant_name, 'funding_souce':biogasplant.funding_souce,
                'country':biogasplant.country, 'region':biogasplant.region, 'district':biogasplant.district,
                'ward':biogasplant.ward, 'village':biogasplant.village, 'other_address_details':biogasplant.other_address_details,
                'type_biogas':biogasplant.type_biogas,'volume_biogas':biogasplant.volume_biogas, 'location':biogasplant.location, 
                'location_estimated':biogasplant.location_estimated, 'current_status':biogasplant.current_status }
            #pdb.set_trace()
            #biogasplant.UIC = data['UIC']
            #biogasplant.biogas_plant_name = data['biogas_plant_name']
            #biogasplant.funding_souce = data['funding_source']
            #biogasplant.country = data['country']
            #biogasplant.region = data['region']
            #biogasplant.district = data['district']
            #biogasplant.ward = data['ward']
            #biogasplant.village = data['village']
            #biogasplant.other_address_details = data['other_address_details']
            #biogasplant.type_biogas = data['type_biogas']
            #biogasplant.volume_biogas = data['volume_biogas']
            #biogasplant.location = Point(data['longitude'],data['latitude'])
            #biogasplant.location_estimated = data["location_estimated"]
            #biogasplant.current_status = data['current_status']
            for fld in fields:
                try:
                    if fld == 'location':
                        field_relations[fld] = Point(data['longitude'],data['latitude'])
                    else:
                        field_relations[fld] = data[fld]
                except:
                    pass

            bb=biogasplant.save()
            if data["contruction_tech"] == "me":
                biogasplant.constructing_technicians.add(UserDetail.objects.get(user=uob) )
            if (data['contact'] is not None): # now link the biogas plant to a contact
                #pdb.set_trace()
                uid = uuid.UUID(hex=data['contact'])
                biogasplant.contact.add(BiogasPlantContact.objects.get( uid = uid) )
            if (data['associated_company'] is not None):
                #biogasplant.associated_company = data['associated_company']]
                pass
            plant_id = biogasplant.plant_id.hex
            #create(first_name=data['firstname'],surname=surname,mobile,contact_type=contact_type, mobile=mobile, email=email)
            bundle.data = {"message":"biogas plant created","uid":plant_id}
        except:
            bundle.data = {"message":"error"}

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=False)
    def edit_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        bundle = self.build_bundle(data={}, request=request)

        data = json.loads( request.read() )
        data = only_keep_fields(data,['biogas_plant_name','contact','funding_souce','funding_source_notes','country','region','district','ward','village','other_address_details','type_biogas','supplier','volume_biogas','location_estimated','QP_status','sensor_status','current_status','verfied','what3words'])
        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        
        try:
            #uid = uuid.UUID(hex=pk) # the id of the job that wants reasigning needs to be included in the URL
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            
            if uob.is_superuser:
                plant_to_edit = BiogasPlant.objects.get(id=pk)

                for itm in data: # for simple text based changes this is very easy - no additional clauses needed
                    setattr(plant_to_edit, itm, data[itm])
                plant_to_edit.save()
                bundle.data = { "message":"Biogas Plant Updated" }
        except:
            pass

        return self.create_response(request, bundle)
    
    

    def dehydrate(self, bundle):
        #pdb.set_trace()
        dat = bundle.obj.contact.values()
        bundle.data['contact'] = [i for i in dat]
        return bundle

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
                bundle.obj = BiogasPlant.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True: # pk=pk,,
                try:
                    
                    bundle.obj = BiogasPlant.objects.get(Q(pk=pk),Q(associated_company__company_id__in = list_of_company_ids_admin[1]) | Q(constructing_technicians__company__company_id__in = list_of_company_ids_admin[1]) ) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['UIC','contact','constructing_technicians','funding_souce','funding_source_notes','country','region','district','ward','village','postcode','other_address_details','type_biogas','supplier','volume_biogas','what3words','location','QP_status','sensor_status','current_status','verfied']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and list_of_company_ids_tech[0] is True ):
                try:
                    bundle.obj = BiogasPlant.objects.get(Q(pk=pk),Q(associated_company__company_id__in = list_of_company_ids_admin[1]) | Q(constructing_technicians__company__company_id__in = list_of_company_ids_admin[1]))
                    #bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_tech[1]) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['UIC','contact','constructing_technicians','funding_souce','funding_source_notes','country','region','district','ward','village','postcode','other_address_details','type_biogas','supplier','volume_biogas','what3words','location','QP_status','sensor_status','current_status','verfied']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="You do not have permission to edit that contact")
                
            else:
                bundle.obj = BiogasPlant.objects.none()
                bundle.data ={}

        bundle = self.full_hydrate(bundle)

        #pdb.set_trace(0)
        return super(BiogasPlantResource, self).obj_update(bundle, user=uob)


    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)

        return super(BiogasPlantResource, self).obj_create(bundle, user=uob)

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
            return object_list.filter(Q(contact__associated_company__company_name__in=company_names) | Q(associated_company__company_name__in=company_names))

        if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            #pdb.set_trace()
            # we want to filter and return only the biogas plants associated with that technican
            #object_list.biogas_plant_detail
            return []