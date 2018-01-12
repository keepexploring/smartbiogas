from django.conf.urls import include, url
from . import views
from tastypie.api import Api
from api import CompanyResource, UserDetailResource, TechnicianDetailResource, BiogasPlantContactResource, BiogasPlantResource, JobHistoryResource, DashboardResource

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())
v1_api.register(UserDetailResource())
v1_api.register(TechnicianDetailResource())
v1_api.register(BiogasPlantContactResource())
v1_api.register(BiogasPlantResource())
v1_api.register(JobHistoryResource())
v1_api.register(DashboardResource())

urlpatterns = [
              # url(r'home/$', views.index_main.as_view(), name='home'),
               url(r'^$', views.index_main.as_view() ,name='home'),
               url(r'^technicians/$', views.Technicians.as_view() ,name='technicians'),
               url(r'^plants/$', views.Plants.as_view() ,name='plants'),
               url(r'^jobs/$', views.Jobs.as_view() ,name='jobs'),
               url(r'^api/', include(v1_api.urls)),
      

]