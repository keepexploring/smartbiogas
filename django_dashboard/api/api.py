from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL
from django_dashboard.api.api_biogas_details import BiogasPlantResource
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
        list_allowed_methods = ['get', 'post']
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
            put=("read","write")
        )

        #def obj_create(self, bundle, **kwargs):
        #    return super(MyModelResource, self).obj_create(bundle, user=bundle.request.user)
    def hydrate(self, bundle):
        pdb.set_trace()
        pass
    
    def obj_create(self, bundle, **kwargs):
        pdb.set_trace()
        return super(CompanyResource, self).obj_create(bundle, user=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        pdb.set_trace()
        return super(CompanyResource, self).obj_update(bundle, user=bundle.request.user)

    def obj_delete(self, bundle, **kwargs):
        pdb.set_trace()
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
    class Meta:
        queryset = TechnicianDetail.objects.all()
        resource_name = 'userdetail'
        excludes = []
        list_allowed_methods = ['post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("write",),
            get=(),
            put=()
            #post=("read write",),
            #get=("read",),
            #put=("read","write")
        )


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
        resource_name = 'Dashboard'
        excludes = []
        list_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
    # def authorized_read_list(self, object_list, bundle):
    #     return object_list.filter(user=bundle.request.user)
        
       