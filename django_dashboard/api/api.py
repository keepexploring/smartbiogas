from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
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
import pdb


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
        pdb.set_trace()

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
                    'phone_number':ALL
                    }
        #filtering = {'username':ALL} # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )

    def dehydrate(self, bundle):
        
        url = bundle.request.build_absolute_uri()
        root_url = url.split('/api')[0]
        if bundle.data['user_photo'] is not None:
            bundle.data['user_photo'] = root_url+ bundle.data['user_photo']
        
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

        return bundle

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
                pass
            else:
                bundle.obj = UserDetail.objects.none()
                bundle.data = {}

        bundle = self.full_hydrate(bundle)
        return bundle

    
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
    

    class Meta:
        queryset = JobHistory.objects.all()
        resource_name = 'jobs'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )

    def dehydrate(self, bundle):
        
        plant_info = bundle.obj.plant.__dict__ # one biogas plant associated with one job
        contact_info = bundle.obj.plant.contact.values()
        constructing_tech = []
        for ii in bundle.obj.plant.constructing_technicians.all():
            ct = ii.__dict__
            #pdb.set_trace()
            ct["company_name"] = [k['company_name'] for k in ii.company.values()] 
            #ct["company_names"] = ii.company.get().company_name  # include company name
            constructing_tech.append(ct)

        fixers = []
        #pdb.set_trace()
        try:
            for ii in bundle.obj.fixers.all():
                fx = ii.__dict__
                fx["company_name"] = [k['company_name'] for k in ii.company.values()] 
                #fx["company_name"] = ii.company.get().company_name  # include company name
                fixers.append(ct)
        except Exception, err:
            print(err)
            traceback.print_exc()
            pdb.set_trace()
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
        bundle.data['fixers'] = [{k:v for  k, v in i.iteritems() if k in fields_to_return_fixers} for i in fixers]

        
        return bundle

    def obj_update(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)
        list_of_company_ids = perm.check_auth_admin()

        return bundle

    def obj_create(self, bundle, **kwargs):
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)

        return bundle

    

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
                return object_list.filter(fixers__user__username=uob.username)
        except:
            pdb.set_trace()
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
    def authorized_read_list(self, object_list, bundle):
    # need to set this so returns the company in the users settings - they can choose any company they are part of
         return object_list.filter(user=bundle.request.user)[0:1]
        
    