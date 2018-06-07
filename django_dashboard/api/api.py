from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs
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
from helpers import datetime_to_string, error_handle_wrapper, only_keep_fields, map_fields, to_serializable, AddressSerializer, raise_custom_error, required_fields
from django.core.paginator import Paginator
from tastypie_actions.actions import actionurls, action
from django_postgres_extensions.models.functions import ArrayAppend, ArrayReplace
from django.contrib.gis.geos import Point
import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
from validate_email import validate_email
from django_dashboard.api.password_management import PasswordManagementResource
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import pdb

multiselect_fields = { "plumber":'PLUMBER',"mason":'MASON',"manager":'MANAGER',"design":'DESIGN','calculations':'CALCULATIONS','tubular':'TUBULAR','fixed_dome':'FIXED_DOME' }
# monkey patch the Resource init method to remove a particularly cpu hungry deepcopy
def patched_resource__init__(self, api_name=None):
    #self.fields = deepcopy(self.base_fields)
    self.fields = {k: copy(v) for k, v in self.base_fields.iteritems()}

    if not api_name is None:
        self._meta.api_name = api_name

Resource.__init__ = patched_resource__init__


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all() # everything in the Techicians database - or use Entry.objects.all().filter(pub_date__year=2006) to restrict what is returned
        resource_name = 'company' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post', 'put']
        filtering = {'company_name':ALL,
                    'username':ALL,
                    'country':ALL,
                    'region':ALL,
                    'district':ALL,
                    'ward':ALL,
                    'village':ALL,
                    'phone_number':ALL
                    } # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read", "write"),
            
        )

        #def obj_create(self, bundle, **kwargs):
        #    return super(MyModelResource, self).obj_create(bundle, user=bundle.request.user)
    def hydrate(self, bundle):
        return bundle

    
    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        
        if uob.is_superuser: # only superusers are able to create companies (basically only admins of the whole system not of individual companies)
            if bundle.data['company_name'] is None:
                bundle.data={}
            else:
                
                exists = Company.objects.all().filter(company_name=bundle.data['company_name']).exists()
                if exists is True:
                    bundle.data={}
                    raise CustomBadRequest(
                    code="403",
                    message="Company name is not unique")
        else:
            bundle.data={}
            raise CustomBadRequest(
                    code="401",
                    message="Only superusers are able to create companies")

                            
        bundle = self.full_hydrate(bundle)

        return super(CompanyResource, self).obj_create(bundle, user=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        #pdb.set_trace()

        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        try:
            bundle.obj = Company.objects.get(pk=pk)
        except KeyError:
            raise NotFound("Object not found")

        if uob.is_superuser: # only superusers are able to create companies (basically only admins of the whole system not of individual companies)
            pass
        else:
            bundle.data={}
            raise CustomBadRequest(
                    code="401",
                    message="Only superusers are able to create companies")

        bundle = self.full_hydrate(bundle)
        return super(CompanyResource, self).obj_update(bundle, user=bundle.request.user)

    def obj_delete(self, bundle, **kwargs):
        #pdb.set_trace()
        pass

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
        # need to put an if in here so superusers can see everything
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        if uob.is_superuser:
            return object_list

        if user_object[0].role.label == 'Company Admin':
            company_object = user_object[0].company.all()
            company_names = [co.company_name for co in company_object]
            return object_list.filter(company_name__in=company_names)

        if user_object[0].role.label == 'Technician':
            company_object = user_object[0].company.all()
            company_names = [co.company_name for co in company_object]
            return object_list.filter(company_name__in=company_names.defer("company_id") )
            
    #def get_object_list(self, request):
        #return super(MyModelResource, self).get_object_list(request).filter(start_date__gte=timezone.now())

class TechnicianDetailResource(ModelResource): # child
    #technicians = fields.OneToOneField(TechnicianDetailResource, 'technicians')
    """This class will return the logged in technician's details - and allow the technician to update it as required"""
    class Meta:
        queryset = TechnicianDetail.objects.all()
        resource_name = 'userdetail'
        excludes = []
        list_allowed_methods = ['get','put']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            #post=("read write",),
            get=("read",),
            put=("read", "write"),
            
        )

    
    def prepend_urls(self):
        return actionurls(self)


    @action(allowed=['get'], require_loggedin=False, static=True)
    def get_profile(self, request, **kwargs):
        self.is_authenticated(request)

        try:
            
            bundle = self.build_bundle(data={}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()

            tech_detail = TechnicianDetail.objects.get(technicians__user = uob)
            user_detail = UserDetail.objects.get(user = uob)

            detail = {}
            detail['technician_id'] = tech_detail.technician_id
            detail['acredit_to_install'] = tech_detail.acredit_to_install
            detail['acredited_to_fix'] = tech_detail.acredited_to_fix
            detail['specialist_skills'] = tech_detail.specialist_skills
            detail['number_jobs_active'] = tech_detail.number_jobs_active
            detail['number_of_jobs_completed'] = tech_detail.number_of_jobs_completed
            detail['status'] = tech_detail.status
            #detail['what3words'] = tech_detail.what3words
            detail['location'] = tech_detail.location
            detail['latitude'] = tech_detail.location.get_y()
            detail['longitude'] = tech_detail.location.get_x() 
            detail['willing_to_travel'] = tech_detail.willing_to_travel
            detail['languages_spoken'] = tech_detail.languages_spoken
            #detail['company'] = user_detail.company.values() # this can be added later
            detail['first_name'] = user_detail.first_name
            detail['last_name'] = user_detail.last_name
            detail['mobile'] = user_detail.phone_number
            detail["email"] = user_detail.email

            bundle.data = detail

        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=True)
    def edit_profile(self, request, **kwargs):
        self.is_authenticated(request)
        
        data = json.loads( request.read() )
        fields = ["mobile", "email","languages_spoken","latitude","longitude","specialist_skills","willing_to_travel"]
        data = only_keep_fields(data, fields)
        ud_fields = ["phone_number","email"]
        td_fields = ["specialist_skills","willing_to_travel"]
        data = map_fields( data, [ ("mobile","phone_number") ] )
        
        try:
            td = { key:item for key, item in data.iteritems() if key in td_fields}
            ud = { key:item for key, item in data.iteritems() if key in ud_fields}
            bundle = self.build_bundle(data={}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            tech_detail = TechnicianDetail.objects.filter(technicians__user = uob)
            user_detail = UserDetail.objects.filter(user = uob)
            tech_detail.update(**td)
            user_detail.update(**ud)
            #pdb.set_trace()
            try:
                tech_detail.update( languages_spoken = data["languages_spoken"] )  # ArrayReplace("languages_spoken", 
            except:
                pass
            #pdb.set_trace()
            if "latitude" in data.keys() and "longitude" in data.keys():
                tech_detail.update(location=Point(data['longitude'],data['latitude']) )
            
            bundle.data = {"message":"Profile updated"}
        except:
            pass

        return self.create_response(request, bundle)
    

    @action(allowed=['put'], require_loggedin=False, static=False) ## This is introduced here to avoid making a breaking change with the app - this function is for admin users to allow them to edit any plant in their company
    def edit_technician(self, request, **kwargs):
        self.is_authenticated(request)
        
        bundle = self.build_bundle(data={}, request=request)

        data = json.loads( request.read() )
        data = only_keep_fields(data,['role','first_name','last_name','mobile','email','region','district','ward','village','other_address_details','acredit_to_install','acredited_to_fix','specialist_skills','what3words','languages_spoken','longitude','latitude'])
        
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
            
            multiselect_fields = { "plumber":'PLUMBER',"mason":'MASON',"manager":'MANAGER',"design":'DESIGN','calculations':'CALCULATIONS','tubular':'TUBULAR','fixed_dome':'FIXED_DOME' }
            if uob.is_superuser:
                tech_to_edit = UserDetail.objects.get(id=pk)
                tech_to_edit_additional_details = tech_to_edit.technician_details
                
                for itm in data: # for simple text based changes this is very easy - no additional clauses needed
                    if itm == 'languages_spoken':
                        try:
                            tech_to_edit_additional_details.update(languages_spoken = data["languages_spoken"] )  # ArrayReplace("languages_spoken", 
                        except:
                            pass
                    elif itm == "latitude":
                        try:
                            tech_to_edit_additional_details.technician_details.update(location=Point(data['longitude'],data['latitude']) )
                        except:
                            pass
                    elif itm in ['role','first_name','last_name','mobile','email','region','district','ward','village','other_address_details']:
                        setattr(tech_to_edit, itm, data[itm])
                    elif itm == 'what3words':
                        setattr(tech_to_edit_additional_details, itm, data[itm])
                    elif itm in ['acredit_to_install','acredited_to_fix','specialist_skills']:
                        choices_to_save = [ multiselect_fields[ii] for ii in data[itm] ]
                        setattr(tech_to_edit_additional_details, itm, choices_to_save)

                tech_to_edit.save()
                tech_to_edit_additional_details.save()
                bundle.data = { "message":"Tech Updated" }
        except:
            pass

        return self.create_response(request, bundle)


    @action(allowed=['get'], require_loggedin=False, static=True)
    def get_status(self, request, **kwargs):
        self.is_authenticated(request)

        #pdb.set_trace()
        try:
            bundle = self.build_bundle(data={}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()

            tech_detail = TechnicianDetail.objects.get(technicians__user = uob)

            bundle.data = {"status":tech_detail.status,"tech_id":str(tech_detail.technician_id)}

        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=False)
    def change_status(self, request, **kwargs):
        self.is_authenticated(request)

        #pdb.set_trace()
        try:
            st = int(kwargs['pk'])
            #job_id = 
        except:
            st = kwargs['pk']

        try:
            bundle = self.build_bundle(data={}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            tech_detail = TechnicianDetail.objects.get(technicians__user = uob)
            if (st is 1):
                tech_detail.status = True
                bundle.data = {"status":True,"tech_id":str(tech_detail.technician_id)}
                
            else:
                tech_detail.status = False
                bundle.data = {"status":False,"tech_id":str(tech_detail.technician_id)}
            tech_detail.save()
        
        except:
            pass

        return self.create_response(request, bundle)





    def obj_update(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)

        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']


        if uob.is_superuser:
            try:
                bundle.obj = TechnicianDetail.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        # an admin can only edit technican's in their company that they are admin for
        else:
            list_of_company_ids = perm.check_auth_admin()
            list_of_company_ids = []

            if list_of_company_ids[0] is True:
                try:
                    bundle.obj = TechnicianDetail.objects.get(pk=pk,technicians__company__company_id__in = list_of_company_ids[1]) # a superuser can edit any technican's record
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="Object not found")
                fields_to_allow_update_on = ['status','what3words','willing_to_travel','acredit_to_install','acredited_to_fix','specialist_skills','max_num_jobs_allowed']
                bundle = keep_fields(bundle, fields_to_allow_update_on)
            else:
                try:
                    bundle.obj = TechnicianDetail.objects.get(pk=pk, technicians__user = uob) # we make sure the record being requested is that of the logged in user
                except:
                    raise CustomBadRequest(
                            code="403",
                            message="Users can only modify their own records, that is the record of the logged in user")

        return super(TechnicianDetailResource, self).obj_update(bundle, user=uob)

    def authorized_read_list(self, object_list, bundle):
        uob = bundle.request.user
        
        return object_list.filter(technicians__user__username=uob.username)


class UserDetailResource(ModelResource): # parent
    technician_details = fields.OneToOneField(TechnicianDetailResource, 'technician_details', related_name="technician_details",null=True, blank=True, full=True)
    user = fields.OneToOneField( User, 'usera', related_name = 'user', null=True, blank=True, full=True )
    # N.B. the related name is the name in the models that 'appears' in the parent class and is used for reverse looku from the child class
    # useful info http://django-tastypie.readthedocs.io/en/latest/tutorial.html#creating-more-resources - this is not reverse look up but provides the background info
    class Meta:  
        queryset = UserDetail.objects.all() # everything in the Techicians database
        resource_name = 'users' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = {'first_name':ALL,
                    'last_name':ALL,
                    'country':ALL,
                    'region':ALL,
                    'district':ALL,
                    'ward':ALL,
                    'village':ALL,
                    'phone_number':ALL,
                    'user': ALL_WITH_RELATIONS,
                    }
        #filtering = {'username':ALL} # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )


    def prepend_urls(self):
        return actionurls(self)


    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_technicians(self, request, **kwargs):
        """get all the techs that are available for a job - this is only available to admins or superusers"""
        self.is_authenticated(request)
        

        try:
            
             # we specify the type of bundle in order to help us filter the action we take before we return
            bundle = self.build_bundle(data={}, request=request)
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech

            users_details = UserDetail.objects.filter(user = uob)[0] # we can use this to get the country of the superuser/admin and then only return relevant techs.
            pending_jobs = PendingJobs.objects.filter(technician__user=uob)
            active_jobs = JobHistory.objects.filter(fixers__user=uob,completed=False)
            num_active_jobs=len(active_jobs)

            #if len(pending_jobs) == 0 and num_active_jobs<1: # the user can not get another job if they have not accepted this one!
            techs = UserDetail.objects.filter(technician_details__status=True, country='Tanzania', ) # technician_details__max_num_jobs_allowed__gt = num_active_jobs - for later at the moment we hardcode to allow only one job at a time
            # use the related_name to look up and filter to ensure they do not have any active or pending jobs
            #bundle = self.build_bundle(obj=techs, request=request)
            #bundle = self.alter_detail_data_to_serialize(request, bundle)
            #pdb.set_trace()
            ##now serialize:
            data_list = []
            for ii in techs:
                #pdb.set_trace()
                try:
                    data = {'company':ii.company.name,
                            'first_name':ii.first_name,
                            'last_name':ii.last_name,
                            'country':ii.country,
                            'village':ii.village,
                            'region':ii.region,
                            'mobile':ii.phone_number.as_international,
                            'uri':'/api/v1/users/' + str(ii.id) + '/',
                            'location': to_serializable(ii.technician_details.location),
                            # 'longitude': ii.technician_details.location.get_x(),
                            # 'latitude': ii.technician_details.location.get_y(),
                            'acredited_to_fix':ii.technician_details.acredited_to_fix,
                            'specialist_skills':ii.technician_details.specialist_skills,
                            'number_jobs_active':ii.technician_details.number_jobs_active,
                            'number_of_jobs_completed':ii.technician_details.number_of_jobs_completed,
                            'status':ii.technician_details.status,
                            'willing_to_travel':ii.technician_details.willing_to_travel,
                            'languages_spoken':ii.technician_details.languages_spoken,
                            'uid':ii.technician_details.technician_id,
                            }
                    data_list.append(data)
                except:
                    pass
            bundle.data['technicians'] = data_list

            #bundle = self.build_bundle(data=bundle.data, request=request)


        except:
            #bundle = self.build_bundle(data={}, request=request)
            pass

        #return UserDetailResource().get_list(request).filter()
        #bundle = self.full_dehydrate(bundle) 
        
        return self.create_response(request, bundle)


    @action(allowed=['post'], require_loggedin=False,static=True)
    def remove_technician_from_database(self, request, **kwargs):
        pass

    

    def dehydrate(self, bundle):
        #pdb.set_trace()
        
        #url = bundle.request.build_absolute_uri()
        #root_url = url.split('/api')[0]
        #if bundle.data['user_photo'] is not None:
        #    bundle.data['user_photo'] = root_url+ bundle.data['user_photo']
        
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
                bundle.obj = UserDetail.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True:
                try:
                    bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_admin[1]) # a superuser can edit any technican's record
                except:
                    flag = 1
                fields_to_allow_update_on = ['first_name','last_name ','user_photo','phone_number','country','region','district','ward','village','postcode','other_address_details']
                bundle = keep_fields(bundle, fields_to_allow_update_on)
            
            # A technician can only update their own details
            if (flag == 1 and list_of_company_ids_tech[0] is True):
                try:
                    bundle.obj = TechnicianDetail.objects.get(pk=pk, technicians__user = uob)
                    #bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_tech[1]) # a superuser can edit any technican's record
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="Object not found")
                fields_to_allow_update_on = ['first_name','last_name ','user_photo','phone_number','country','region','district','ward','village','postcode','other_address_details']
                bundle = keep_fields(bundle, fields_to_allow_update_on)
            else:
                bundle.obj = TechnicianDetail.objects.none()
                bundle.data ={}

        return super(UserDetailResource, self).obj_update(bundle, user=uob)

    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)
        list_of_company_ids_admin = perm.check_auth_admin()
        list_of_company_ids_tech = perm.check_auth_tech()

        
        if uob.is_superuser:
            pass
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True:
                # we need to filter this to allow admins to only be able to create users for companies they are admin for.
                pass
            else:
                bundle.obj = UserDetail.objects.none()
                bundle.data = {}
        pdb.set_trace()
        bundle = self.full_hydrate(bundle)
        
        return super(UserDetailResource, self).obj_create(bundle, user=uob)

    @action(allowed=['post'], require_loggedin=False,static=True)
    def create_technician(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        data = only_keep_fields(data,['first_name','last_name','mobile','phone_number','email','user_photo','country','region','district','ward','village','postcode','other_address_details','role','acredit_to_install','acredited_to_fix','specialist_skills','status','what3words','willing_to_travel','max_num_jobs_allowed','languages_spoken','username','password'])
        required_fields(data,['first_name','last_name','username','mobile'] )
        if 'phone_number' in data.keys():
            data['mobile'] = data['phone_number']
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        #user_object = UserDetail.objects.filter(user=uob)
        #part_of_groups = uob.groups.all()
        #perm = Permissions(part_of_groups)
        #list_of_company_ids_admin = perm.check_auth_admin()
        #list_of_company_ids_tech = perm.check_auth_tech()

        if uob.is_superuser:
            try: # validate the selected username
                if User.objects.filter(username=data['username']).exists():
                    raise_custom_error({"error":"Username not unique someone else is using it. Do please try a different username"}, 500)

                if validate_email(data['username']) is True:
                    is_mobile_email = 'email'
                elif carrier._is_mobile(number_type(phonenumbers.parse(data['username']))):
                    is_mobile_email = 'mobile'
                else:
                    raise_custom_error({"error":"You need to provide a username and password. The username must be a valid email or mobile number (with international calling code)"}, 500)
            except:
                raise_custom_error({"error":"You need to provide a username and password. The username must be a valid email or mobile number (with international calling code)"}, 500)

            try:
                logged_in_as = uob.userdetail.logged_in_as
                user = User.objects.create_user(username=data['username'], email=data['username'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'] )    
                userdetail = UserDetail.objects.create(user=user, logged_in_as = logged_in_as )
                try: # include this for the time being as a lot of the old users don't have this field
                    userdetail.company.add(logged_in_as)
                except:
                    pass
                tech_additional_details=TechnicianDetail(technicians=userdetail)
                tech_additional_details.save()
                
                for itm in data: # for simple text based changes this is very easy - no additional clauses needed
                    if itm == 'languages_spoken':
                        try:
                            tech_additional_details.languages_spoken = data["languages_spoken"]   # ArrayReplace("languages_spoken", 
                        except:
                            pass
                    elif itm == "latitude":
                        try:
                            tech_additional_details.location = Point(data['longitude'],data['latitude']) 
                        except:
                            pass
                    elif itm in ['role','first_name','last_name','mobile','email','region','district','ward','village','other_address_details']:
                        setattr(userdetail, itm, data[itm])
                    elif itm in ['what3words', 'status','willing_to_travel']:
                        setattr(tech_additional_details, itm, data[itm])
                    elif itm in ['acredit_to_install','acredited_to_fix','specialist_skills']:
                        choices_to_save = [ multiselect_fields[ii] for ii in data[itm] ]
                        setattr(tech_additional_details, itm, choices_to_save)
                        #reset_code = PasswordManagementResource.generate_reset_code(uob)
                
                userdetail.save()
                tech_additional_details.save()
                bundle.data = {"message":"User created", "user_id":userdetail.id }
            except:
                raise_custom_error({"error":"Your request has not succeeded. Sorry not to be more helpful. Goodbye."}, 500)

            return self.create_response(request, bundle)
        else:
            raise_custom_error({"error":"You are not authorised"}, 403)

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        if uob.is_superuser:
            return object_list

        if user_object[0].role.label == 'Company Admin': # return all the people associated with this company
            company_object = user_object[0].company.all()
            company_names = [co.company_name for co in company_object]
            return object_list.filter(company__company_name__in=company_names)

        if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
            return object_list.filter(user__username=uob.username)
          

class JobHistoryResource(ModelResource):
    #plant = fields.ToManyField(BiogasPlantResource, 'plant', null=True, blank=True, full=True)
    #fixers = fields.ManyToManyField(UserDetailResource, 'fixerss', related_name="fixerss", null=True, blank=True, full=True)
    
    class Meta:
        queryset = JobHistory.objects.all()
        resource_name = 'jobs'
        excludes = []
        list_allowed_methods = ['get', 'post','put']
        filtering = {'job_id':ALL,
                    'completed':ALL,
                    'job_status':ALL,
                    'verification_of_engagement':ALL,
                    'due_date':ALL,
                    'date_completed':ALL,
                    'fixers':ALL_WITH_RELATIONS,
                    'plant':ALL_WITH_RELATIONS,
                    }
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )

    def prepend_urls(self):
        return actionurls(self)

    @action(allowed=['get'], require_loggedin=False,static=False) #static=True if you don't want to include an id in the url
    def find_new_tech(self, request, **kwargs):
        """Find a new technician when they accepted but did not take"""
        pdb.set_trace()
        self.is_authenticated(request)
        #objs = JobHistoryResource.get_list(self, request, **kwargs)
        pdb.set_trace()
        pass

    @action(allowed=['post'], require_loggedin=True)
    def tech_request_help(self, request, **kwargs):
        """Find a new technician when they accepted but did not take"""
        self.is_authenticated(request)
        pdb.set_trace()
        pass

    @action(allowed=['post'], require_loggedin=False, static=False)
    def abandon_job(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        data = only_keep_fields(data,['reasons','additional_comments'])
        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        
        
        bundle = self.build_bundle(data={}, request=request)
        try:
            uid = uuid.UUID(hex=pk)
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            current_job = JobHistory.objects.filter(fixers__user=uob, job_id=uid).filter(Q(completed=False) | Q(completed = None))[0]
            user_detail = UserDetail.objects.get(user=uob)
            current_job.rejected_job.add(user_detail) # this is
            current_job.fixers.remove(user_detail)
            #fixers  = JobHistory.objects.filter(fixers__user=uob, job_id=uid).filter(Q(completed=False) | Q(completed = None))[0]
            current_job.completed = False
            current_job.job_status = 1
            current_job.verification_of_engagement = False
            current_job.priority = True
            if "help_type" in data.keys():
                current_job.reason_abandoning_job = str(current_job.reason_abandoning_job) + "\n \n" + datetime_to_string(datetime.datetime.now()) + "\n" + data['reasons']
            
            if "additional_comments" in data.keys():
                current_job.other = str(current_job.other) + "\n \n" + datetime_to_string(datetime.datetime.now()) +" [abandon_job] "  + "\n" + data['additional_comments']

            current_job.save()
            bundle.data = { "message":"job_abandoned", "job_id": pk }

        except:
            pass

        return self.create_response(request, bundle)


    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_abandoned_jobs(self, request, **kwargs):
        self.is_authenticated(request)
        bundle = self.build_bundle(data={}, request=request)

        #pdb.set_trace()

        try:
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            #pdb.set_trace()
            if uob.is_superuser:
                #abandoned_jobs = JobHistory.objects.exclude(rejected_job=None).filter(Q(fixers=None))
                abandoned_jobs = JobHistory.objects.filter(Q(fixers=None)) # for now we include all jobs that do not have fixers
                #serialized_jobs = json.loads( serializers.serialize('json', abandoned_jobs) )
                jobs_to_send = []
                #pdb.set_trace()
                for ab in abandoned_jobs:
                    serialized_jobs = {}
                    serialized_jobs["job_id"] = ab.job_id.hex
                    serialized_jobs["fault_description"] = ab.fault_description
                    serialized_jobs["description_help_need"] = ab.description_help_need
                    serialized_jobs["dispute_raised"] = ab.dispute_raised
                    serialized_jobs["fault_class"] = ab.fault_class
                    serialized_jobs["plant"] = ab.plant
                    serialized_jobs["reason_abandoning_job"] = ab.reason_abandoning_job
                    serialized_jobs["assistance"] = ab.assistance
                    serialized_jobs["date_flagged"] = ab.date_flagged
                    serialized_jobs["location"] = to_serializable(ab.plant.location)
                    serialized_jobs["ward"] = ab.plant.ward
                    serialized_jobs["village"] = ab.plant.village
                    serialized_jobs["country"] = ab.plant.country
                    serialized_jobs["region"] = ab.plant.region
                    serialized_jobs["district"] = ab.plant.district
                    serialized_jobs["other_address_details"] = ab.plant.other_address_details
                    contacts = []
                    for cc in ab.plant.contact.all():
                        contact = {}
                        contact["first_name"] = cc.first_name
                        contact["surname"] = cc.surname
                        contact["mobile"] = cc.mobile
                        contact["contact_type"] = cc.contact_type
                        contacts.append(contact)
                    serialized_jobs["contacts"] = contacts
                    jobs_to_send.append(serialized_jobs)

                bundle.data = {'data':jobs_to_send}
            else:
                bundle.data = {}

        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=False)
    def reassign_abandoned_job(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        data = only_keep_fields(data,['technician'])
        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        bundle = self.build_bundle(data={}, request=request)

        try:
            uid = uuid.UUID(hex=pk) # the id of the job that wants reasigning needs to be included in the URL
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            if uob.is_superuser:
                job_to_reassign = JobHistory.objects.filter(job_id=uid)[0]
                fixer_id = int(data['technician'].split("/")[-2])
                user_to_reassign_to = UserDetail.objects.get(user__id=fixer_id) # the user id of the fixer is used to look up the user object
                job_to_reassign.fixers.add(user_to_reassign_to)
                bundle.data = { "message":"Job Reassigned" }
            else:
                 bundle.data = { "error":"Permission Denied" }
        except:
            pass

        return self.create_response(request, bundle)



    @action(allowed=['post'], require_loggedin=False,static=True)
    def register_new_ward_village(self, request, **kwargs):
        pass

    @action(allowed=['put'], require_loggedin=False,static=False)
    def remove_technician_from_job(self, request, **kwargs):
        pass

    @action(allowed=['put'], require_loggedin=False,static=False)
    def edit_job(self, request, **kwargs):
        self.is_authenticated(request)
        
        bundle = self.build_bundle(data={}, request=request)

        data = json.loads( request.read() )
        data = only_keep_fields(data,['due_date','completed','dispute_raised','fault_description','other','priority','fault_class'])
        
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        if 'due_date' in data.keys():
            data['due_date'] = timezone.make_aware(datetime.datetime.utcfromtimestamp(data['due_date']), timezone = timezone.utc)
        
        try:
            uid = uuid.UUID(hex=pk) # the id of the job that wants reasigning needs to be included in the URL
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            
            if uob.is_superuser:
                job_to_edit = JobHistory.objects.filter(job_id=uid)[0]
                
                for itm in data: # for simple text based changes this is very easy - no additional clauses needed
                    setattr(job_to_edit, itm, data[itm])
                job_to_edit.save()
        except:
            pass

        return self.create_response(request, bundle)


    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_active_jobs(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        bundle = self.build_bundle(data={}, request=request)

        try:
            
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            #pdb.set_trace()
            current_jobs = JobHistory.objects.filter(fixers__user=uob, completed=False).order_by('-date_flagged')

            job_list = []
            for job in current_jobs:
                #pdb.set_trace()
                job_record = {}
                job_record["job_id"] = job.pk.hex
                
                job_record["install_date"] = datetime_to_string(job.plant.install_date)
                job_record["date_flagged"] = datetime_to_string(job.date_flagged)
                job_record["date_accepted"] = datetime_to_string(job.date_accepted)
                
                job_record["job_status"] = job.job_status
                job_record["fault_description"] = job.fault_description
                job_record["other"] = job.other
                job_record["priority"] = job.priority
                job_record["fault_class"] = job.fault_class
                job_record["district"] = job.plant.district
                job_record["ward"] = job.plant.ward
                job_record["volume"] = job.plant.volume_biogas
                try:
                    job_record["longitude"] = job.plant.location.get_x()
                    job_record["latitude"] = job.plant.location.get_y()
                except:
                    pass
                
                try:
                    job_record["supplier"] = job.plant.supplier.name
                except:
                    pass
        
                job_record["QP_status"] = job.plant.QP_status
                job_record["sensor_status"] = job.plant.sensor_status
                job_record["current_status"] = job.plant.current_status
                job_record["type_biogas"] = job.plant.type_biogas
                
                job_list.append(job_record)
            
            bundle.data = {'data':job_list}
        except Exception as e:
            #print(e)
            pass

        return self.create_response(request, bundle)

    
    @action(allowed=['post'], require_loggedin=False,static=True)
    def get_historical_jobs(self, request, **kwargs):
        self.is_authenticated(request)

        data = json.loads( request.read() )
        page=int(data['page']) # add in some error handling here
        per_page = int(data["per_page"])

        bundle = self.build_bundle(data={}, request=request)

        try:
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            historical_jobs = JobHistory.objects.filter(fixers__user=uob, completed=True)
            pag = Paginator(historical_jobs, per_page)
            historical_jobs=pag.page(page)
            #serialized_jobs = json.loads( serializers.serialize('json', historical_jobs) )
            job_list = []
            
            for job in historical_jobs:
                job_record = {}
                job_record["job_id"] = job.pk.hex
                
                job_record["install_date"] = datetime_to_string(job.plant.install_date)
                job_record["job_status"] = job.job_status
                job_record["fault_description"] = job.fault_description
                job_record["other"] = job.other
                job_record["district"] = job.plant.district
                job_record["ward"] = job.plant.ward
                job_record["volume"] = job.plant.volume_biogas
                try:
                    job_record["longitude"] = job.plant.location.get_x()
                    job_record["latitude"] = job.plant.location.get_y()
                except:
                    pass
                
                try:
                    job_record["supplier"] = job.plant.supplier.name
                except:
                    pass
        
                job_record["QP_status"] = job.plant.QP_status
                job_record["sensor_status"] = job.plant.sensor_status
                job_record["current_status"] = job.plant.current_status
                job_record["type_biogas"] = job.plant.type_biogas
                
                job_list.append(job_record)
            
            bundle.data = {'data':job_list}
            bundle.data['pagination'] = {"item_count":pag.count, "page_count":pag.num_pages,"page_num":page,"has_next":historical_jobs.has_next(),"has_previous":historical_jobs.has_previous()}

        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['post'], require_loggedin=False,static=False)
    def call_for_assistance(self, request, **kwargs):
        self.is_authenticated(request)
        data = json.loads( request.read() )
        data = only_keep_fields(data,['help_type','additional_comments'])
        #pdb.set_trace()
        try:
            pk = int(kwargs['pk'])
            #job_id = 
        except:
            pk = kwargs['pk']

        uid = uuid.UUID(hex=pk)
        bundle = self.build_bundle(data={}, request=request)

        try:
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            current_job = JobHistory.objects.filter(fixers__user=uob, job_id=uid).filter(Q(completed=False) | Q(completed = None))[0]
            current_job.job_status = 5
            current_job.priority = True
            if "help_type" in data.keys():
                current_job.description_help_need = str(current_job.description_help_need) + "\n \n" + datetime_to_string(datetime.datetime.now()) + "\n" + data['help_type']
            
            if "additional_comments" in data.keys():
                current_job.other = str(current_job.other) + "\n \n" + datetime_to_string(datetime.datetime.now()) + " [call_for_assistance] " + "\n" + data['additional_comments']

            current_job.save()
            bundle.data = {"message":"We have requested additional assistance for you","job_id":pk}

        except:
            pass

        return self.create_response(request, bundle)



    @action(allowed=['post'], require_loggedin=False, static=False)
    def job_complete(self, request, **kwargs):
        self.is_authenticated(request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        data = only_keep_fields(data,['issue','additional_comments'])
        try:
            pk = int(kwargs['pk'])
            #job_id = 
        except:
            pk = kwargs['pk']
        
        try:
            uid = uuid.UUID(hex=pk)
            bundle = self.build_bundle(data={}, request=request)
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            current_job = JobHistory.objects.filter(fixers__user=uob, job_id=uid).filter(Q(completed=False) | Q(completed = None))[0]
            if "issue" in data.keys():
                current_job.fault_description = str(current_job.fault_description) + "\n \n" + datetime_to_string(datetime.datetime.now()) + "\n" + data['issue']
            
            if "additional_comments" in data.keys():
                current_job.other = str(current_job.other) + "\n \n" + datetime_to_string(datetime.datetime.now()) + " [job_complete] "+ "\n" + data['additional_comments']
            current_job.completed = True
            current_job.job_status = 4
            current_job.priority = False
            current_job.save()
            bundle.data = {"message":"job completed", "job_id":pk}
        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['get'], require_loggedin=True)
    def get_excluded_technicians(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass

    @action(allowed=['get'], require_loggedin=True)
    def adjust_rating(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass
        
    @action(allowed=['get'], require_loggedin=True)
    def raise_dispute(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass

    @action(allowed=['get'], require_loggedin=True)
    def raise_service_complaint(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass

    @action(allowed=['post'], require_loggedin=True)
    def get_admins(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass


    def dehydrate(self, bundle):

        #pdb.set_trace()
        
        plant_info = bundle.obj.plant.__dict__ # one biogas plant associated with one job
        contact_info = bundle.obj.plant.contact.values()
        constructing_tech = []
        constructing_tech_obj = bundle.obj.plant.constructing_technicians.all()
        for ii in constructing_tech_obj:
            ct = ii.__dict__
            #pdb.set_trace()
            ct["company_name"] = [k['company_name'] for k in ii.company.values()] 
            #ct["company_names"] = ii.company.get().company_name  # include company name
            constructing_tech.append(ct)

        fixers_list = []
        fixers_obj = bundle.obj.fixers.all()
       
        try:
            for ii in fixers_obj:
                fx = ii.__dict__
                fx["company_name"] = [k['company_name'] for k in ii.company.values()] 
                #fx["company_name"] = ii.company.get().company_name  # include company name
                fixers_list.append(fx)
        except Exception, err:
            print(err)
            traceback.print_exc()
            #pdb.set_trace()
            pass

        #cconstructing_tech = [i.values() for i in bundle.obj.plant.constructing_technicians ]
        

        
        fields_to_return_plant_info = ['country','region','district','ward','village','postcode','neighbourhood','other_address_details','type_biogas','size_biogas','what3words','plant_status']
        fields_to_return_contact_info = ['contact_type','first_name','surname','mobile','associated_company']
        fields_to_return_fixers = ['role','first_name','last_name','phone_number','company_name','user_id']
        fields_to_return_constructing_tech = ['role','first_name','last_name','phone_number','company_name','user_id']

        #pdb.set_trace()
        bundle.data['system_info'] = plant_info
        bundle.data['contact_info'] = [{k:v for  k, v in i.iteritems() if k in fields_to_return_contact_info} for i in contact_info]
        bundle.data['constructing_tech'] = [{k:v for  k, v in i.iteritems() if k in fields_to_return_constructing_tech} for i in constructing_tech]
        bundle.data['fixers'] = [{k:v for  k, v in i.iteritems() if k in fields_to_return_fixers} for i in fixers_list]

        
        return bundle

    def obj_update(self, bundle, **kwargs):
        

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
                bundle.obj = JobHistory.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True:
                try:
                    bundle.obj = JobHistory.objects.get(pk=pk,fixers__company__company_id__in = list_of_company_ids_admin[1]) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['due_date','completed','job_status','verification_of_engagement','fault_description','other','overdue_for_acceptance','priority','fault_class']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and list_of_company_ids_tech[0] is True ):
                try:
                    bundle.obj = JobHistory.objects.get(pk=pk, fixers__user = uob)
                    #bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_tech[1]) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['completed','fault_description','other','priority','fault_class','assistance','due_date']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="You do not have permission to edit that job")
                
            else:
                bundle.obj = TechnicianDetail.objects.none()
                bundle.data ={}

        bundle = self.full_hydrate(bundle)

        #pdb.set_trace(0)
        return super(JobHistoryResource, self).obj_update(bundle, user=uob)

    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)

        return super(JobHistoryResource, self).obj_create(bundle, user=uob)

    

    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
        try:
            uob = bundle.request.user
            user_object = UserDetail.objects.filter(user=uob)
            if uob.is_superuser:
                return object_list

            if user_object[0].role.label == 'Company Admin': # return all the people associated with this company
                #pdb.set_trace()
                company_object = user_object[0].company.all()
                company_names = [co.company_name for co in company_object]
                return object_list.filter(plant__contact__associated_company__company_name__in=company_names)

            if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
                #pdb.set_trace()
                pass
                return object_list.filter(fixers__user=uob)
        except:
            #pdb.set_trace()
            pass

class DashboardResource(ModelResource):
    class Meta:
        queryset =  Dashboard.objects.all()
        resource_name = 'dashboard'
        excludes = []
        list_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )


    
# 

   # def authorized_read_list(self, object_list, bundle):
    # need to set this so returns the company in the users settings - they can choose any company they are part of
     #   uob = bundle.request.user
      #  user_object = UserDetail.objects.filter(user=uob)
      #  company_ids = 
      #  company_to_display = 
      #  return object_list.filter(company__company_id=)
        
    