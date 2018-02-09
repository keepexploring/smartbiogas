from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django_react.views import LoginView
from forms import LoginForm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'),{'authentication_form':LoginForm},name='login'),
    url(r'^login2/$', LoginView.as_view(), name='login2'), 
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^', include('django_dashboard.urls')),
    url(r'^dashboard/', include('django_dashboard.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    url('^searchableselect/', include('searchableselect.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
