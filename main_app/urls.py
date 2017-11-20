from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home', views.home, name='home2'),
    url(r'^dashboard', views.dashboard_main, name='dashboard_main'),
]
