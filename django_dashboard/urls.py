from django.conf.urls import include, url
from . import views
from tastypie.api import Api
from api.api import CompanyResource, UserDetailResource, TechnicianDetailResource, JobHistoryResource, DashboardResource
from api.api_biogas_contact import BiogasPlantContactResource
from api.api_biogas_details import BiogasPlantResource
from api.validate import ValidateToken
from django_dashboard.views import RegionAutocomplete, CountryAutocomplete, ContinentAutocomplete, DistrictAutocomplete, WardAutocomplete, VillageAutocomplete, SupplierAutocomplete, VolumeAutocomplete 

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())
v1_api.register(UserDetailResource())
v1_api.register(TechnicianDetailResource())
v1_api.register(BiogasPlantContactResource())
v1_api.register(BiogasPlantResource())
v1_api.register(JobHistoryResource())
v1_api.register(DashboardResource())
v1_api.register(ValidateToken())

urlpatterns = [
              # url(r'home/$', views.index_main.as_view(), name='home'),
               url(r'^$', views.index_main.as_view() ,name='home'),
               url(r'^technicians/$', views.Technicians.as_view() ,name='technicians'),
               url(r'^plants/$', views.Plants.as_view() ,name='plants'),
               url(r'^jobs/$', views.Jobs.as_view() ,name='jobs'),
               url(r'^api/', include(v1_api.urls)),
               url(r'^region-autocomplete/$', RegionAutocomplete.as_view(), name='region-autocomplete'),
               url(r'^district-autocomplete/$', DistrictAutocomplete.as_view(), name='district-autocomplete'),
               url(r'^ward-autocomplete/$', WardAutocomplete.as_view(), name='ward-autocomplete'),
               url(r'^village-autocomplete/$', VillageAutocomplete.as_view(), name='village-autocomplete'),
               url(r'^country-autocomplete/$', CountryAutocomplete.as_view(), name='country-autocomplete'),
               url(r'^continent-autocomplete/$', ContinentAutocomplete.as_view(), name='continent-autocomplete'),
               url(r'^supplier-autocomplete/$', SupplierAutocomplete.as_view(), name='supplier-autocomplete'),
               url(r'^volume-autocomplete/$', VolumeAutocomplete.as_view(), name='volume-autocomplete'),
      
]