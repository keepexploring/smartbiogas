from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from forms import LoginForm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'),{'authentication_form':LoginForm},name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^', include('django_dashboard.urls')),
    url(r'^dashboard/', include('django_dashboard.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
]
