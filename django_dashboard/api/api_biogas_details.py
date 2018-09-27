from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, AddressData
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.paginator import Paginator
from helpers import Permissions, only_keep_fields, if_empty_fill_none, to_serializable, to_serializable_location, raise_custom_error, BiogasPlantSerialiser
from helpers import map_fields, to_serializable, CustomBadRequest, Permissions, ContactDetailsSerializer
from django.db.models import Q
from tastypie.constants import ALL
from tastypie_actions.actions import actionurls, action
# from django_dashboard.api.api_biogas_contact import BiogasPlantContactResource
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
from django_dashboard.api.api_address_resource import AddressResource

import pdb

class BiogasPlantContactResource(ModelResource):
    biogas_plant_details = fields.ManyToManyField('BiogasPlantResource', 'biogas_plant_detail',null=True, blank=True, full=True)

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

        try:
            uid = uuid.UUID(hex=pk)
        except:
            raise CustomBadRequest(
                        code="400",
                        message="UID not valid")

        uob = bundle.request.user
        perm = Permissions(uob)
        logged_in_as_company = perm.get_company_scope()

        if uob.is_superuser:
            try:
                bundle.obj = BiogasPlantContact.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if perm.is_admin():
                try:
                    bundle.obj = BiogasPlantContact.objects.get( pk=pk,associated_company =  logged_in_as_company) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['contact_type','first_name','surname','mobile','email','associated_company']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and perm.is_technician() is True ):
                try:
                    bundle.obj = BiogasPlantContact.objects.get( pk=pk,associated_company = logged_in_as_company)
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
    @transaction.atomic
    def create_biogas_contact(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["contact_type", "first_name", "surname","mobile","country","village","region","district","ward","latitude","longitude","what3words","UIC","email"]
        _schema_ = schema['create_biogas_contact']
        vv= Validator(_schema_)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )
        
        
        data = only_keep_fields(data, fields)
        data = if_empty_fill_none(data, fields)
        #pdb.set_trace()
        address_keywords = get_address_keywords() # these are all the words people might send relating to setting an address e.g. region, country etc
        address_object = create_address_object()
        address_object_instance = address_object()
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            perm = Permissions(uob)

            if ( uob.is_superuser or perm.is_technician() or perm.is_admin() or perm.is_global_admin() ):

                contact = BiogasPlantContact() # if plant_id is a field we need to add it to the plant that has been specified
                contact.first_name = data['first_name']
                contact.surname = data['surname']
                contact.mobile = data['mobile']
                contact.contact_type = data['contact_type']
                contact.registered_by = uob.userdetail
                for ak in address_keywords:
                    if ak in data.keys():
                        setattr( address_object_instance, ak, data[ak] )

                if "latitude" in data.keys() and "longitude" in data.keys():
                    address_object_instance.set_location(data['longitude'],data['latitude'])
                # contact.region = data['region']
                # contact.district = data['district']
                # contact.ward = data['ward']
                # contact.village = data['village']
                _address_object = map_address_to_database(address_object_instance)
                _address_object.save()
                contact.address = _address_object
                bb=contact.save()
                # try: # we now have a set_location method in the address_object that can be used, so we can do this before if we prefer
                    
                #         contact.address.set_location(data['longitude'],data['latitude'])
                #         contact.address.save()
                #         contact.save()
                # except:
                #     pass

                uuid = contact.uid

                #create(first_name=data['firstname'],surname=surname,mobile,contact_type=contact_type, mobile=mobile, email=email)
                bundle.data = {"message":"contact created","uid":uuid.hex}
        except:
            raise CustomBadRequest(
                        code="500",
                        message="Object not created")

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=True)
    def edit_biogas_contact(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["contact_type", "first_name", "surname","mobile","country","village","region","district","ward","latitude","longitude","what3words","UIC","email"]
        _schema_ = schema['edit_biogas_contact']
        vv= Validator(_schema_)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )

        data = only_keep_fields(data, fields)

        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        try:
            uid = uuid.UUID(hex=pk)
        except:
            raise CustomBadRequest(
                        code="400",
                        message="UID not valid")

        uid = uuid.UUID(hex=pk)

        address_keywords = get_address_keywords() 
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            perm = Permissions(uob)

            if ( uob.is_superuser or perm.is_technician() or perm.is_admin() or perm.is_global_admin() ):
                contact = BiogasPlantContact.objects.get( uid=uid )
                address_object = map_database_to_address_object( contact.address )
                for itm in data:
                    if itm in ["contact_type", "first_name", "surname","mobile"]:
                        setattr(contact, itm, data[itm])
                    elif itm in address_keywords:
                        setattr(address_object, itm, data[itm])
                
                _address_object = map_address_to_database(address_object)
                _address_object.save()
                contact.address = _address_object
                contact.save()
                bundle.data = { "message":"contact edited","uid":contact.uid.hex }

        except:
            raise CustomBadRequest(
                        code="403",
                        message="Object not found")

        return self.create_response(request, bundle)
        


    @action(allowed=['post'], require_loggedin=False, static=True)
    def find_biogas_contact(self, request, **kwargs):
        #pdb.set_trace()
        self.is_authenticated(request)
        
        data = json.loads( request.read() )
        data = only_keep_fields(data, ["mobile"] )
        
        try:
            bundle = self.build_bundle(data={}, request=request)
            uob = bundle.request.user
            perm = Permissions(uob)
            company = perm.get_company_scope()

            if (uob.is_superuser or perm.is_global_admin()):
                contacts = BiogasPlantContact.objects.filter(mobile=data['mobile'])

            elif perm.is_admin():
                contacts = BiogasPlantContact.objects.filter(mobile=data['mobile'], registered_by__company = company)

            elif perm.is_technician():
                contacts = BiogasPlantContact.objects.filter(mobile=data['mobile'], registered_by = uob.userdetail )
            
            else:
                raise CustomBadRequest(
                        code="401",
                        message="you are not authorised")

            data_to_return = []
            for cc in contacts:
                biogas_owner = {}
                biogas_owner['first_name'] = cc.first_name
                biogas_owner['surname'] = cc.surname
                biogas_owner['mobile'] = cc.mobile
                biogas_owner['contact_type'] = cc.contact_type.name
                biogas_owner['email'] = cc.email
                #biogas_owner['contact'] = to_serializable(cc.uid)[0]
                biogas_owner['contact']= cc.uid.hex
                biogas_owner['location'] = to_serializable(cc.address.location)
                biogas_owner['address'] = map_address_to_json_from_database(cc.address)
                biogas_owner['longitude'] = cc.address.get_x()
                biogas_owner['latitude'] = cc.address.get_y()
                
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
        except Exception as e:
            print(e)
            raise CustomBadRequest(
                        code="403",
                        message="Record does not exist")

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

    # @action(allowed=['put'], require_loggedin=False, static=False)
    # def create_biogas_plant(self, request, **kwargs):
    #     self.is_authenticated(request)
    #     data = json.loads( request.read() )
    #     data = only_keep_fields(data, ["firstname", "surname","mobile","owner","village","region","district","wards","what3words"])
    #     bundle = self.build_bundle(data={}, request=request)
    #     try:
    #         uid = uuid.UUID(hex=pk)
    #         uob = bundle.request.user
    #         part_of_groups = uob.groups.all()
    #         perm = Permissions(part_of_groups)
    #         list_of_company_ids_admin = perm.check_auth_admin()
    #         list_of_company_ids_tech = perm.check_auth_tech()
    #         contact = BiogasPlantContact.objects.create(first_name,surname,mobile,contact_type)

    #     except:
    #         pass

    #     return self.create_response(request, bundle)


    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()

        user_object = UserDetail.objects.filter(user=uob)
        
        if ( uob.is_superuser or perm.is_global_admin() ):
            pass

        else:
            bundle.data = {}

        return super(BiogasPlantContactResource, self).obj_create(bundle, user=bundle.request.user)
        
    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
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
            #return object_list.filter(associated_company__company_name__in=company_names)
            return object_list.filter(biogas_plant_detail__associated_company = company)

        if perm.is_technician(): # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            return []

    def authorized_read_detail(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
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
            #return object_list.filter(associated_company__company_name__in=company_names)
            return object_list.filter(biogas_plant_detail__associated_company = company)

        if perm.is_technician(): # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            return []


class BiogasPlantResource(ModelResource):

    #contact = fields.ToManyField('BiogasPlantContactResource', 'contact',null=True, blank=True) # full=True

    #contact = fields.ManyToManyField(BiogasPlantContactResource,'contact')
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
                    'verfied': ALL,
                    'install_date':ALL,
                    'id':ALL,
                    }
                    
        ordering = ['funding_souce','supplier','QP_status','current_status','funding_souce','sensor_status','volume_biogas','type_biogas','size_biogas','country','region','district','ward','village','other_address_details','verfied','install_date']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        paginator_class = Paginator

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

    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_adopted_plants(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
    
        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()
        bundle = self.build_bundle(data={}, request=request)

        try:
            biogas_plants = BiogasPlant.objects.filter(adopted_by = uob.userdetail)
            biogas_plant_serialised = BiogasPlantSerialiser(biogas_plants, many=True)
            data_list = map_serialised_address(biogas_plant_serialised.data)
            for plant in data_list:
                plant = map_serialised_address(plant)
            bundle.data['data'] = data_list
        except:
            raise_custom_error({"error":"Serialisation error"}, 500)

        return self.create_response(request, bundle)

    
    @action(allowed=['put'], require_loggedin=False,static=False)
    def orphan_or_adopt(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)
        data = json.loads( request.read() )
        data = only_keep_fields(data,['orphan_or_adopt'])
        _schema = schema['orphan_or_adopt']
        vv= Validator(_schema)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )

        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']
        
        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()

        if uob.is_superuser or perm.is_global_admin():
            try:
                biogas_plant = BiogasPlant.objects.get( id = pk )
            except:
                raise_custom_error({"error":"Biogas plant not found"}, 404)
        elif perm.is_admin() or perm.is_technician():
            try:
                biogas_plant = BiogasPlant.objects.get( id = pk, associated_company__in = [company] )
            except:
                raise_custom_error({"error":"Biogas plant not found in your company"}, 404)
        
        if data['orphan_or_adopt'] == 'adopt':
            biogas_plant.adopted_by = uob.userdetail
        elif data['orphan_or_adopt'] == 'orphan':
            biogas_plant.adopted_by = None
        
        biogas_plant.save()
        bundle.data = { "message":"biogas plant adopted", "id": pk }

        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False,static=True)
    def get_biogas_plants(self, request, **kwargs):
        """Gte the biogas plants of an owner form their mobile number"""
        self.is_authenticated(request)
        
        data = json.loads( request.read() )
        
        _schema_ = schema['get_biogas_plants']
        vv= Validator(_schema_)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )

        mobile=data['mobile']
        bundle = self.build_bundle(data={}, request=request)

        
             # we specify the type of bundle in order to help us filter the action we take before we return
        uob = bundle.request.user
        #if uob.is_superuser:
        perm = Permissions(uob)
        company = perm.get_company_scope()
        #bundle.data['technicians'] = data_list
        if uob.is_superuser or perm.is_global_admin():
            biogas_plants = BiogasPlant.objects.filter(contact__mobile__in=[mobile])
        elif perm.is_admin() or perm.is_technician():
            biogas_plants = BiogasPlant.objects.filter(associated_company__in = [company]).filter(contact__mobile__in=[mobile])
        else:
            raise_custom_error({"error":"You not have authorisation"}, 401)
        try:
            biogas_plant_serialised = BiogasPlantSerialiser(biogas_plants, many=True)
            data_list = map_serialised_address(biogas_plant_serialised.data)
            for plant in data_list:
                plant = map_serialised_address(plant)
            bundle.data['data'] = data_list
        except:
            raise_custom_error({"error":"Server error"}, 500)
            # for bi in biogas_plants:
            #     data = { 
            #             "owner": [{"first_name":ii.first_name, "surname":ii.surname, "mobile":ii.mobile, "contact_type":ii.contact_type.name} for ii in bi.contact.all()],
            #             "biogas_plant_name": bi.biogas_plant_name,
            #                 "associated_company": bi.associated_company,
            #             "address": map_address_to_json_from_database(bi.address),
            #             # "country":bi.country,
            #             # "region": bi.region,
            #             # "district":bi.district,
            #             # "ward": bi.ward,
            #             # "village":bi.village,
            #             "type_biogas":bi.type_biogas,
            #             "supplier":bi.supplier,
            #             "volume_biogas":bi.volume_biogas,
            #             "QP_status":bi.QP_status,
            #             "sensor_status":bi.sensor_status,
            #             "current_status":bi.current_status,
            #             "verfied":bi.verfied,
            #             "uri":"/api/v1/biogasplant/"+str(bi.id)+"/",
            #             "location_estimated":bi.location_estimated,
            #             "location": to_serializable_location(bi.address.location),
            #             }
            #     data_list.append(data)
            
        

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False, static=True)
    def search_for_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ['UIC']
        data = only_keep_fields(data, fields)
        bundle = self.build_bundle(data={}, request=request)

        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()
        try:
            if uob.is_superuser or perm.is_global_admin():
                biogas_plant = BiogasPlant.objects.filter(UIC=data['UIC'])
            elif perm.is_admin() or perm.is_technician():
                biogas_plant = BiogasPlant.objects.filter(UIC=data['UIC'])
                if len( biogas_plant[0].associated_company.all() ) != 0:
                    biogas_plant.filter( associated_company__in = [company] )
            biogas_plant = biogas_plant[0]
        except:
            raise_custom_error({"error":"No biogas plant found with that UIC"}, 500)
        try:
            
            biogas_plant_serialised = BiogasPlantSerialiser(biogas_plant)
            bundle.data = map_serialised_address(biogas_plant_serialised.data)
        except:
            raise CustomBadRequest(
                    code="404",
                    message="UIC submitted does not exist")

        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False, static=True)
    @transaction.atomic
    def create_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["UIC", "biogas_plant_name","adopt", "associated_company","contact","funding_source","latitude","longitude","country","village","region","district","ward","what3words","type_biogas","volume_biogas","install_date","other_address_details","current_status","contruction_tech","location_estimated"]
        _schema_ = schema['create_biogas_plant']
        vv= Validator(_schema_)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )
        
        data = only_keep_fields(data, fields)
        data = if_empty_fill_none(data, fields)

        fields = data.keys()

        address_keywords = get_address_keywords() # these are all the words people might send relating to setting an address e.g. region, country etc
        address_object = create_address_object()
        address_object_instance = address_object()
        bundle = self.build_bundle(data={}, request=request)
        try:
            uob = bundle.request.user
            perm = Permissions(uob)
            company = perm.get_company_scope() 

            if ( ( BiogasPlant.objects.filter(UIC=data['UIC']).exists() ) is (False or data['UIC'] is None) ) :
                biogasplant = BiogasPlant()
            else:
                raise CustomBadRequest(
                        code="400",
                        message="This sensor is already registered on the system - please search for it if you want to modify the record")

             # if plant_id is a field we need to add it to the plant that has been specified
            # field_relations = {'UIC': biogasplant.UIC, 'biogas_plant_name':biogasplant.biogas_plant_name, 'funding_souce':biogasplant.funding_souce,
            #     'country':biogasplant.country, 'region':biogasplant.region, 'district':biogasplant.district,
            #     'ward':biogasplant.ward, 'village':biogasplant.village, 'other_address_details':biogasplant.other_address_details,
            #     'type_biogas':biogasplant.type_biogas,'volume_biogas':biogasplant.volume_biogas, 'location':biogasplant.location, 
            #     'location_estimated':biogasplant.location_estimated, 'current_status':biogasplant.current_status, 'adopted_by':biogasplant.adopted_by }
            
            for itm in data:
                if itm in ['UIC','biogas_plant_name','funding_souce','volume_biogas','location_estimated','current_status','type_biogas','install_date']:
                    setattr(biogasplant, itm, data[itm])

                elif itm in address_keywords:
                    setattr(address_object_instance, itm, data[itm])

                elif itm in ['location']:
                    address_object_instance.set_location( data['longitude'],data['latitude'] )

                elif itm in ['adopt']:
                    if data['adopt'] == True:
                        setattr(biogasplant, 'adopted_by', uob.userdetail)
             # whatever company the one doing the registering is part of, we assign the biogas plant to that company
            address_object_to_save = map_address_to_database(address_object_instance)
            address_object_to_save.save()
            biogasplant.address = address_object_to_save
            biogasplant.save()
            biogasplant.associated_company.add(company) # associate the plant with the company who creates the record - this can be changed
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

            # for fld in fields:
            #     try:
            #         if fld == 'location':
            #             biogasplant.set_location(data['longitude'],data['latitude'])
            #         elif fld == 'adopt':
            #             if data['adopt'] == True:
            #                 field_relations['adopted_by'] = uob.userdetail
            #         else:
            #             field_relations[fld] = data[fld]
            #     except:
            #         pass

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
            raise raise_custom_error({"error":"Server error"}, 500)

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=False)
    @transaction.atomic
    def edit_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)

        data = json.loads( request.read() )
        data = only_keep_fields(data,['biogas_plant_name','contact','funding_souce','funding_source_notes','country','region','district','ward','village','other_address_details','type_biogas','supplier','volume_biogas','location_estimated','QP_status','sensor_status','current_status','verfied','what3words'])
        
        _schema_ = schema['edit_biogas_plant']
        vv= Validator(_schema_)
        if not vv.validate(data):
            errors_to_report = vv.errors
            raise CustomBadRequest( code="field_error", message=errors_to_report )

        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        
        try:
            #uid = uuid.UUID(hex=pk) # the id of the job that wants reasigning needs to be included in the URL
            uob = bundle.request.user
            perm = Permissions(uob)
            company = perm.get_company_scope()
            
            if (uob.is_superuser or perm.is_global_admin() ):
                plant_to_edit = BiogasPlant.objects.get(id=pk)
            elif perm.is_admin():
                plant_to_edit = BiogasPlant.objects.get( Q(id=pk) & ( Q(adopted_by__company=company) | Q(adopted_by__company=None) ) )
            else:
                raise CustomBadRequest(
                        code="401",
                        message="Unauthorized")

            address_keywords = get_address_keywords() # these are all the words people might send relating to setting an address e.g. region, country etc
            address_object = map_database_to_address_object( plant_to_edit.address )

            for itm in data: # for simple text based changes this is very easy - no additional clauses needed
                if itm in address_keywords:
                    setattr(address_object, itm, data[itm])
                elif itm in ['contact']:
                    contact_uuid = uuid.UUID(hex = data[itm])
                    plant_contact = BiogasPlantContact.objects.get(uid=contact_uuid)
                    plant_to_edit.contact.add(plant_contact)
                else:
                    setattr(plant_to_edit, itm, data[itm])
            _address_object = map_address_to_database(address_object)
            _address_object.save()
            plant_to_edit.address = _address_object
            plant_to_edit.save()
            bundle.data = { "message":"Biogas Plant Updated" }
        except:
            raise CustomBadRequest(
                        code="403",
                        message="Object not found")

        return self.create_response(request, bundle)
    
    
    def dehydrate(self, bundle):
        data_object = bundle.obj.contact.all()
        contacts = ContactDetailsSerializer(data_object, many=True).data
        for ob in contacts:
            ob = map_serialised_address(ob)
        bundle.data['contact'] = contacts
        return bundle

    def obj_update(self, bundle, **kwargs):
        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        uob = bundle.request.user
        perm = Permissions(uob)
        company = perm.get_company_scope()

        if ( uob.is_superuser or perm.is_global_admin() ):
            try:
                bundle.obj = BiogasPlant.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if perm.is_admin() is True: # pk=pk,,
                try:
                    
                    bundle.obj = BiogasPlant.objects.get(Q(pk=pk),Q(associated_company__company_id__in = list_of_company_ids_admin[1]) | Q(constructing_technicians__company__company_id__in = list_of_company_ids_admin[1]) ) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['UIC','contact','constructing_technicians','funding_souce','funding_source_notes','country','region','district','ward','village','postcode','other_address_details','type_biogas','supplier','volume_biogas','what3words','location','QP_status','sensor_status','current_status','verfied']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and perm.is_technician() is True ):
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

    @action(allowed=['get'], require_loggedin=False, static=False) ## This is introduced here to avoid making a breaking change with the app - this function is for admin users to allow them to edit any plant in their company
    @transaction.atomic
    def get_single_biogas_plant(self, request, **kwargs):
        self.is_authenticated(request)

        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        try:
            bundle = self.build_bundle(data={}, request=request)
            uob = bundle.request.user
            perm = Permissions(uob)
            company = perm.get_company_scope()
        except:
            raise_custom_error({"error":"Biogas plant object not found"}, 404)

        if ( uob.is_superuser or perm.is_global_admin() ):
            plant = BiogasPlant.objects.get( id = pk )
        elif perm.is_admin(): # return all the people associated with this company
            plant = BiogasPlant.objects.get( id = pk, associated_company = company )
        elif perm.is_technician(): # only return the user info of the logged in technican
            plant = BiogasPlant.objects.get( id = pk, associated_company = company, adopted_by = uob.userdetail )
            
        else:
            raise_custom_error({"error":"You do not have permission"}, 401)

        try:
            serialised_biogas_plant = BiogasPlantSerialiser(plant).data
            bundle.data = map_serialised_address(serialised_biogas_plant)
        except:
            raise_custom_error({"error":"Serialisation error"}, 500)

        return self.create_response(request, bundle)

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)

        try:
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
        except:
            raise raise_custom_error({"error":"Server error"}, 500)

    def authorized_read_detail(self, object_list, bundle):

        try:
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
        except:
            raise raise_custom_error({"error":"Server error"}, 500)