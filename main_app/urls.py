from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home', views.home, name='home2'),
    url(r'^dashboard', views.dashboard_main, name='dashboard_main'),
    url(r'^view3', views.good_old_view, name='view3'),
    url(r'^view1', TemplateView.as_view(template_name='view1.html'),name='view1'),
]
