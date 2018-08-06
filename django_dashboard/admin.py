# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models

from .models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, TechnicianDetail, BiogasPlant, JobHistory, Dashboard, PendingJobs, \
    CardTemplate, Card, PendingAction, UtilisationStatus, LowGasPressure, TrendChangeDetectionPDecrease, TrendChangeDetectionPIncrease, \
    BiogasSensorStatus, AutoFault, DataConnection, IndictorJoinTable, RegisteredNode, IndicatorsTemplate, IndicatorObjects

from django.contrib.admin import widgets
from dynamic_raw_id.admin import DynamicRawIDMixin

from bootstrap_datepicker.widgets import DatePicker
#from datetimepicker.widgets import DateTimePicker
from django_dashboard.forms import UserForm, BiogasForm, CompanyForm, UserDetailForm
from django import forms
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

# class MyAdminSite(AdminSite):
#     # Text to put at the end of each page's <title>.
#     site_title = ugettext_lazy('SmartBiogas Admin')

#     # Text to put in each page's <h1> (and above login form).
#     site_header = ugettext_lazy('SmartBiogas Administration')

#     # Text to put at the top of the admin index page.
#     index_title = ugettext_lazy('SmartBiogas Administration')


class TechnicianDetailAdmin(admin.StackedInline):
    model = TechnicianDetail
    #list_display = ('number_jobs_active','number_of_jobs_completed','location')
    #list_filter = ('number_jobs_active','number_of_jobs_completed','location')
    def queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(TechnicianDetailAdmin, self).queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        if request.role == 'TECHNICIAN':
            return qs.filter(technicans=request.user)
   
        if request.role == 'COMPANY_ADMIN':
            return qs.filter(technicans=request.company)

class PendingJobsAdmin(admin.ModelAdmin): # could make a stacked inline??
    model = PendingJobs
    list_display = ('biogas_plant','technician','job_id','datetime_created','job_details','accepted','technicians_rejected',)
    list_filter = ('biogas_plant','technician','job_id','datetime_created','job_details','accepted','technicians_rejected',)
    search_fields = ('biogas_plant','technician','job_id','datetime_created','job_details','accepted','technicians_rejected',)
   

class UserDetailAdmin(admin.ModelAdmin): # admin.StackedInline
    #inlines = (TechnicianDetailAdmin,)
    model = UserDetail
    form = UserDetailForm
    inlines = [TechnicianDetailAdmin,]
    readonly_fields=('first_name','last_name')
    list_display = ('role','company_title','first_name','last_name','phone_number','region','district','ward','village','neighbourhood','other_address_details','datetime_created')
    list_filter = ('role','first_name','last_name','phone_number','region','district','ward','village','neighbourhood','other_address_details')
    #ordering = ('first_name','last_name','role','phone_number','country','region','district','ward','village','neighbourhood','other_address_details','datetime_created')
    filter_horizontal = ('company',)
    #form = UserForm


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    form = CompanyForm
    list_display = ('company_name','region','district','ward','village','neighbourhood','other_address_details','phone_number', 'emails', 'other_info')
    list_filter = ('company_name','region','district','ward','village','neighbourhood','other_address_details','emails')
    search_fields = ('company_name','region','district','ward','village','neighbourhood','other_address_details','emails','phone_number')


class DashboardAdmin(admin.ModelAdmin):
    model = Dashboard
    list_display = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')
    list_filter = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')
    search_fields = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')


class JobForm(forms.ModelForm):
    # date_flagged = forms.DateTimeField(
    #     widget=DateTimePicker(options = {'format': '%Y-%m-%d %H:%M'}),
    # )
    class Meta:
        model = JobHistory
        exlude = ()
        fields = '__all__'

    #def clean(self):
     #   pass

class JobHistoryInline(admin.TabularInline):
   model = JobHistory
   form = JobForm
   filter_horizontal = ('fixers',)

#    formfield_overrides = {
#         models.DateField: {'widget': DatePicker(
#             options={
#                 "format": "mm/dd/yyyy",
#                 "autoclose": True
#             }
#         )
#         }
#         #models.DateTimeField: {'widget':DateTimePicker(
#         #    options = {'format': '%Y-%m-%d %H:%M'}
#         #)}
#     }

class JobsAdmin(admin.ModelAdmin):
    model = JobHistory 
    list_display= ('plant','job_status','job_id','client_feedback_star','priority','assistance','date_flagged','due_date','date_completed','completed',)
    list_filter= ('plant','job_status','job_id','client_feedback_star','priority','assistance','date_flagged','due_date','date_completed','completed',)
    search_fields= ['job_id',]

    

   #widgets = {
       #     'date_flagged': widgets.AdminDateWidget(),
        #}

class BiogasPlantsAdmin(admin.ModelAdmin):
    form = BiogasForm
    inlines = [JobHistoryInline,]
    list_display = ('get_contact','mobile_num','contact_type','plant_id','type_biogas','volume_biogas','region','district','ward','village','neighbourhood','other_address_details','location')
    list_filter = ('volume_biogas','region','district','ward','village','neighbourhood','other_address_details')
    search_fields = ('get_contact','mobile_num','contact_type','type_biogas','volume_biogas','region','district','ward','village','neighbourhood','other_address_details')
    filter_horizontal = ('contact','constructing_technicians',)


class BiogasPlantContactAdmin(admin.ModelAdmin):
    model = BiogasPlantContact
    list_display = ('uid','associated_company','contact_type','first_name','surname','mobile','email')
    list_filter = ('uid','associated_company','contact_type','first_name','surname','mobile','email')
    search_fields = ('uid','associated_company','contact_type','first_name','surname','mobile','email')
    dynamic_raw_id_fields = ('associated_company',)
    #form = UserForm


class IndicatorObjectsAdmin(admin.ModelAdmin):
    model = IndicatorObjects
    list_display = ('biogas_plant','value','info','status','created','updated')
    list_filter = ('biogas_plant','value','info','status','created','updated')
    search_fields = ('biogas_plant','value','info','status','created','updated')


class IndicatorsTemplateAdmin(admin.ModelAdmin):
    model = IndicatorsTemplate
    #inlines = [IndicatorObjectsAdmin,]
    list_display = ('template_id','type_indicator','title','description','units','image','created','updated')
    list_filter = ('template_id','type_indicator','title','description','units','image','created','updated')
    search_fields = ('template_id','type_indicator','title','description','units','image','created','updated')

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','surname','mobile','email','biogas_owner')
    list_filter = ('first_name','surname','mobile','email','biogas_owner')
    search_fields = ('first_name','surname','mobile','email','biogas_owner')

class CardAdmin(admin.TabularInline):
    model = Card
    list_display = ('card_template','user','value','position','template_id','created','updated')
    list_filter = ('card_template','user','value','position','template_id','created','updated')
    search_fields = ('card_template','user','value','position','template_id','created','updated')

class CardTemplateAdmin(admin.ModelAdmin):
    model = CardTemplate
    inlines = [CardAdmin,]
    list_display = ('id','company','name','title','description','card_type','entity_type','image','created','updated')
    list_filter = ('id','company','name','title','description','card_type','entity_type','image','created','updated')
    search_fields = ('id','company','name','title','description','card_type','entity_type','image','created','updated')

class UtilisationStatusAdmin(admin.TabularInline):
    model = UtilisationStatus
    list_display = ('utilisation_status','utilisation_status_info','created')
    list_filter = ('utilisation_status','utilisation_status_info','created')
    search_fields = ('utilisation_status','utilisation_status_info','created')

class LowGasPressureAdmin(admin.TabularInline):
    model = LowGasPressure
    list_display = ('low_gas_pressure_status','low_gas_pressure_info','created')
    list_filter = ('low_gas_pressure_status','low_gas_pressure_info','created')
    search_fields = ('low_gas_pressure_status','low_gas_pressure_info','created')

class TrendChangeDetectionPDecreaseAdmin(admin.TabularInline):
    model = TrendChangeDetectionPDecrease
    list_display = ('trend_change_detection_pdecrease','trend_change_detection_pdecrease_info','created')
    list_filter = ('trend_change_detection_pdecrease','trend_change_detection_pdecrease_info','created')
    search_fields = ('trend_change_detection_pdecrease','trend_change_detection_pdecrease_info','created')

class TrendChangeDetectionPIncreaseAdmin(admin.TabularInline):
    model = TrendChangeDetectionPIncrease
    list_display = ('trend_change_detection_pincrease','trend_change_detection_pincrease_info','created')
    list_filter = ('trend_change_detection_pincrease','trend_change_detection_pincrease_info','created')
    search_fields = ('trend_change_detection_pincrease','trend_change_detection_pincrease_info','created')

class BiogasSensorStatusAdmin(admin.TabularInline):
    model = BiogasSensorStatus
    list_display = ('sensor_status','sensor_status_info','created')
    list_filter = ('sensor_status','sensor_status_info','created')
    search_fields = ('sensor_status','sensor_status_info','created')

class AutoFaultAdmin(admin.TabularInline):
    model = AutoFault
    list_display = ('auto_fault_detection','auto_fault_detection_info','created')
    list_filter = ('auto_fault_detection','auto_fault_detection_info','created')
    search_fields = ('auto_fault_detection','auto_fault_detection_info','created')

class DataConnectionAdmin(admin.TabularInline):
    model = DataConnection
    list_display = ('data_connection_with_plant','data_connection_with_plant_info','created')
    list_filter = ('data_connection_with_plant','data_connection_with_plant_info','created')
    search_fields = ('data_connection_with_plant','data_connection_with_plant_info','created')

class IndicatorAdmin(admin.ModelAdmin):
    model = IndictorJoinTable
    inlines = [ UtilisationStatusAdmin, LowGasPressureAdmin, TrendChangeDetectionPDecreaseAdmin, TrendChangeDetectionPIncreaseAdmin, \
        BiogasSensorStatusAdmin, AutoFaultAdmin, DataConnectionAdmin, DataConnectionAdmin ]
    list_display = ('plant',)
    list_filter = ('plant',)
    search_fields = ('plant',)

class PendingActionsAdmin(admin.ModelAdmin):
    model = PendingAction
    list_display = ('id','card', 'is_complete', 'entity_type', 'message', 'alert_type','created','updated')
    list_filter = ('id','card', 'is_complete', 'entity_type', 'message', 'alert_type','created','updated')
    search_filter = ('id','card', 'is_complete', 'entity_type', 'message', 'alert_type','created','updated')

class RegisteredNodeAdmin(admin.ModelAdmin):
    model = RegisteredNode
    list_display = ('UIC', 'channel', 'band', 'mode', 'nw_key')
    list_filter = ('UIC', 'channel', 'band', 'mode', 'nw_key')
    search_filter = ('UIC', 'channel', 'band', 'mode', 'nw_key')
#admin.ModelAdmin.ordering = ()
#admin_site = MyAdminSite()
admin.site.site_header = 'SmartBiogas Admin'
admin.site.register(Company, CompanyAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(JobHistory, JobsAdmin)
admin.site.register(PendingJobs, PendingJobsAdmin)
#admin.site.register(TechnicianDetail, TechnicianDetailAdmin)
admin.site.register(BiogasPlant, BiogasPlantsAdmin)
admin.site.register(BiogasPlantContact, BiogasPlantContactAdmin)
#admin.site.register(CardTemplate, CardTemplateAdmin)
admin.site.register(CardTemplate, CardTemplateAdmin)
admin.site.register(IndictorJoinTable, IndicatorAdmin)
admin.site.register(PendingAction, PendingActionsAdmin)
admin.site.register(IndicatorsTemplate, IndicatorsTemplateAdmin)
admin.site.register(IndicatorObjects, IndicatorObjectsAdmin)

#admin.site.register(Users, UserAdmin)

