from tastypie.resources import ModelResource
from django_dashboard.models import Technicians, TechnitionRealtime, Users, BiogasPlants, JobHistory
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL


class TechnicanResource(ModelResource):
    class Meta:
        queryset = Technicians.objects.all() # everything in the Techicians database
        resource_name = 'technicians' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = {'username':ALL} # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        


class Technition_realtimeResource(ModelResource):
    class Meta:
        queryset = TechnitionRealtime.objects.all()
        resource_name = 'realtime'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        

class UserResource(ModelResource):
    class Meta:
        queryset = Users.objects.all()
        resource_name = 'users'
        excludes = []
        list_allowed_methods = ['get', 'post']
        filtering = { "title":ALL }
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
        


class BiogasPlants(ModelResource):
    class Meta:
        queryset = BiogasPlants.objects.all()
        resource_name = 'biogas_plants'
        excludes = []
        list_allowed_methods = ['get', 'post']
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read","write")
        )
       

class JobHistory(ModelResource):
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
        