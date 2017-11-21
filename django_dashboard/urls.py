from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
        url(r'^home/', views.HomeDashboard.as_view(),name='home'),
        url(r'^', views.index_view, name="index_view"),
]