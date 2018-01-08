from django.conf.urls import include, url
from . import views

urlpatterns = [
              # url(r'home/$', views.index_main.as_view(), name='home'),
               url(r'^$', views.index_main.as_view() ,name='home'),
               url(r'^technicians/$', views.Technicians.as_view() ,name='technicians'),
               url(r'^plants/$', views.Plants.as_view() ,name='plants'),
               url(r'^jobs/$', views.Jobs.as_view() ,name='jobs'),

]