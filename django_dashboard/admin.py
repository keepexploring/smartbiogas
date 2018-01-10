# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Technicians, TechnitionRealtime, Users, BiogasPlants, JobHistory, Company, Dashboard

class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('company_name', 'company_address1','company_address2','phone_number', 'emails', 'other_info')
    list_filter = ('company_name', 'company_address1','emails')
    search_fields = ('company_name', 'company_address1','company_address2','emails','phone_number')

class DashboardAdmin(admin.ModelAdmin):
    model = Dashboard

# Register your models here.
class Technition_realtimeInline(admin.StackedInline):
    model = TechnitionRealtime
    #list_display = ('number_jobs_active','number_of_jobs_completed','location')
    #list_filter = ('number_jobs_active','number_of_jobs_completed','location')

class TechniciansAdmin(admin.ModelAdmin):
    inlines = (Technition_realtimeInline,)
    list_display = ('technician_id', 'first_name','last_name','phone_number','nearest_town','specialist_skills','datetime_created')
    list_filter = ('technician_id', 'first_name','last_name','phone_number','nearest_town')
    search_fields = ('technician_id', 'first_name','last_name','phone_number','nearest_town')

class JobHistoryInline(admin.TabularInline):
   model = JobHistory

class BiogasPlantsAdmin(admin.ModelAdmin):
    inlines = [JobHistoryInline,]
    list_display = ('plant_id','type_biogas','size_biogas','town','description_location','postcode','location')
    list_filter = ('type_biogas','size_biogas','town')
    search_fields = ('type_biogas','size_biogas','town')

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','surname','mobile','email','biogas_owner')
    list_filter = ('first_name','surname','mobile','email','biogas_owner')
    search_fields = ('first_name','surname','mobile','email','biogas_owner')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Technicians, TechniciansAdmin)
admin.site.register(BiogasPlants, BiogasPlantsAdmin)
admin.site.register(Users, UserAdmin)

