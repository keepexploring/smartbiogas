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
from helpers import only_keep_fields, if_empty_fill_none, Permissions, map_fields, to_serializable, CustomBadRequest
from tastypie_actions.actions import actionurls, action
import json
from django_dashboard.api.validators.validator_patterns import schema
from helpers import Permissions
from cerberus import Validator
import uuid
from django.db import transaction
from django_dashboard.api.addressmapper import get_address_keywords, create_address_object, map_database_to_address_object, map_address_to_database, map_address_to_json_from_database, map_serialised_address

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
            return object_list.filter(associated_company__company = company)

        if perm.is_technician(): # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            return []