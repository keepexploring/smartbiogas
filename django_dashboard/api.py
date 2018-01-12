from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL


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
        filtering = {'username':ALL} # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )


class UserDetailResource(ModelResource):
    class Meta:
        queryset = UserDetail.objects.all() # everything in the Techicians database
        resource_name = 'technicians' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post']
        #filtering = {'username':ALL} # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        


class TechnicianDetailResource(ModelResource):
    class Meta:
        queryset = TechnicianDetail.objects.all()
        resource_name = 'TechnicianDetail'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        

class BiogasPlantContactResource(ModelResource):
    class Meta:
        queryset = BiogasPlantContact.objects.all()
        resource_name = 'BiogasPlantContact'
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = { "title":ALL }
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        


class BiogasPlantResource(ModelResource):
    class Meta:
        queryset = BiogasPlant.objects.all()
        resource_name = 'BiogasPlant'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
       

class JobHistoryResource(ModelResource):
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

class DashboardResource(ModelResource):
    class Meta:
        queryset =  Dashboard.objects.all()
        resource_name = 'Dashboard'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        
       