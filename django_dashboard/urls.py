from django.conf.urls import include, url
from . import views
from tastypie.api import Api
from api import TechnicanResource, Technition_realtimeResource, UserResource, BiogasPlants, JobHistory

v1_api = Api(api_name='v1')
v1_api.register(TechnicanResource())
v1_api.register(Technition_realtimeResource())
v1_api.register(UserResource())
v1_api.register(BiogasPlants())
v1_api.register(JobHistory())


urlpatterns = [
              # url(r'home/$', views.index_main.as_view(), name='home'),
               url(r'^$', views.index_main.as_view() ,name='home'),
               url(r'^technicians/$', views.Technicians.as_view() ,name='technicians'),
               url(r'^plants/$', views.Plants.as_view() ,name='plants'),
               url(r'^jobs/$', views.Jobs.as_view() ,name='jobs'),
               url(r'^api/', include(v1_api.urls)),
      

]