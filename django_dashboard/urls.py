from django.conf.urls import include, url
from . import views

urlpatterns = [
               url(r'home/$', views.index_main.as_view(), name='home'),
               url(r'^', views.index_main.as_view() ,name='home2'),
]