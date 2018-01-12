# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, TechnicianDetail, BiogasPlant, JobHistory, Dashboard


class TechnicianDetailAdmin(admin.StackedInline):
    model = TechnicianDetail
    #list_display = ('number_jobs_active','number_of_jobs_completed','location')
    #list_filter = ('number_jobs_active','number_of_jobs_completed','location')


class UserDetailAdmin(admin.ModelAdmin): # admin.StackedInline
    #inlines = (TechnicianDetailAdmin,)
    model = UserDetail
    inlines = [TechnicianDetailAdmin,]
    list_display = ('first_name','last_name','phone_number','nearest_town','datetime_created')
    list_filter = ('first_name','last_name','phone_number','nearest_town')



class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('company_name', 'company_address1','company_address2','phone_number', 'emails', 'other_info')
    list_filter = ('company_name', 'company_address1','emails')
    search_fields = ('company_name', 'company_address1','company_address2','emails','phone_number')


class DashboardAdmin(admin.ModelAdmin):
    model = Dashboard
    list_display = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')
    list_filter = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')
    search_fields = ('company', 'created_at', 'plants', 'active', 'faults', 'avtime', 'jobs', 'fixed')

class JobHistoryInline(admin.TabularInline):
   model = JobHistory

class BiogasPlantsAdmin(admin.ModelAdmin):
    inlines = [JobHistoryInline,]
    list_display = ('plant_id','type_biogas','size_biogas','town','description_location','postcode','location')
    list_filter = ('type_biogas','size_biogas','town')
    search_fields = ('type_biogas','size_biogas','town')

class BiogasPlantContactAdmin(admin.ModelAdmin):
    model = BiogasPlantContact

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','surname','mobile','email','biogas_owner')
    list_filter = ('first_name','surname','mobile','email','biogas_owner')
    search_fields = ('first_name','surname','mobile','email','biogas_owner')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
#admin.site.register(TechnicianDetail, TechnicianDetailAdmin)
admin.site.register(BiogasPlant, BiogasPlantsAdmin)
admin.site.register(BiogasPlantContact, BiogasPlantContactAdmin)
#admin.site.register(Users, UserAdmin)

