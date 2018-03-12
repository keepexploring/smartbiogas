from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from helpers import Permissions
from django.db.models import Q
from tastypie.constants import ALL
from helpers import keep_fields
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from django_dashboard.api.api import TechnicianDetailResource, UserDetailResource
from tastypie_actions.actions import actionurls, action
from helpers import remove_fields
from django.core import serializers
import uuid
import json
#from django_dashboard.api.api_biogas_contact import BiogasPlantContactResource

import pdb

class PendingJobsResource(ModelResource):

    #contact = fields.ToManyField(BiogasPlantContactResource, 'contact',null=True, blank=True, full=True)

    #contact = fields.ManyToManyField(BiogasPlantContactResource)
    biogas_plant = fields.ForeignKey(BiogasPlantResource,'biogas_plant')
    technician = fields.ForeignKey(UserDetailResource,'technician')


    def prepend_urls(self):
        return actionurls(self)

    @action(allowed=['put'], require_loggedin=False, static=False)
    def accept_job(self, request, **kwargs):
        
        self.is_authenticated(request)

        try:
            pk = int(kwargs['pk'])
            #job_id = 
        except:
            pk = kwargs['pk']


        
        try:

            uid = uuid.UUID(hex=pk) # introduce some error handling here in case the form of pk is wrong

        #pdb.set_trace()
            bundle = self.build_bundle(data={'job_id': kwargs['pk']}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            #obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
            pending_job = PendingJobs.objects.get(job_id=uid) # job_id is the primary key

            #pdb.set_trace()
            history = JobHistory(job_id=uid,plant=pending_job.biogas_plant)
            if pending_job is not None:
                history = JobHistory()
                history.job_id=uid
                history.plant=pending_job.biogas_plant
                history.save()
                history.fixers.add(pending_job.technician)
                history.date_flagged=pending_job.datetime_created
                history.job_status=2
                history.fault_description=pending_job.job_details
                history.rejected_jobs=pending_job.technicians_rejected
                his=history.save()
                #JobHistory.objects.create(job_id=uid, plant=pending_job.biogas_plant, fixers=pending_job.technician,,job_status=2,fault_description=pending_job.job_details,rejected_jobs=pending_job.technicians_rejected) # job_status=2 means the job is now being resolved
                deleted = pending_job.delete()
                # send_message_to_customer() - to inform them that their job has been accepted and a tech will be in touch soon
        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=False, static=False)
    def reject_job(self, request, **kwargs):
        self.is_authenticated(request)

        try:
            pk = int(kwargs['pk'])
            #job_id = 
        except:
            pk = kwargs['pk']


        

        try:
            uid = uuid.UUID(hex=pk) # introduce some error handling here in case the form of pk is wrong

            #pdb.set_trace()
            bundle = self.build_bundle(data={'job_id': kwargs['pk']}, request=request)
             # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()
            #obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
            pending_job = PendingJobs.objects.get(job_id=uid) # job_id is the primary key

            if pending_job is not None:
                pending_job.technician = None
                pending_job.save()

                bundle.data = {"message":"job_rejected","job_id":pk}
        except:
            pass
        

        return self.create_response(request, bundle)

    @action(allowed=['get'], require_loggedin=False, static=True)
    def get_unassigned_pending_jobs(self, request, **kwargs):
        self.is_authenticated(request)
        
        bundle = self.build_bundle(data={}, request=request)
        uob = bundle.request.user
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)
        list_of_company_ids_admin = perm.check_auth_admin()
        list_of_company_ids_tech = perm.check_auth_tech()

        if uob.is_superuser:
            try:
                pending_jobs = PendingJobs.objects.filter(technician__user=None)
                serialized_jobs = json.loads( serializers.serialize('json', pending_jobs) )
                all_jobs = []
                for nn,ii in enumerate(serialized_jobs):
                    job = {}
                    job['uri'] = '/api/v1/biogasplants/'+str(ii['fields']['biogas_plant']) +'/'
                    job['region'] = pending_jobs[nn].biogas_plant.region
                    job['district'] = pending_jobs[nn].biogas_plant.district
                    job['ward'] = pending_jobs[nn].biogas_plant.ward
                    job['volume'] = pending_jobs[nn].biogas_plant.volume_biogas
                    job['longitude'] = pending_jobs[nn].biogas_plant.location.get_x()
                    job['latitude'] = pending_jobs[nn].biogas_plant.location.get_y()
                    job['QP_status'] = pending_jobs[nn].biogas_plant.QP_status
                    job['sensor_status'] = pending_jobs[nn].biogas_plant.sensor_status
                    job["current_status"] = pending_jobs[nn].biogas_plant.current_status
                    install_date = pending_jobs[nn].biogas_plant.install_date
                    if install_date is not None:
                        job['install_date']=install_date.strftime("%Y-%m-%d %H:%M:%S")
                    job['type_biogas'] = pending_jobs[nn].biogas_plant.type_biogas
                    job['uid'] = uuid.UUID(ii['pk']).hex
                    job['job_details'] = ii['fields']['job_details']
                    job['date_created'] = ii['fields']['datetime_created']
                    job["technician"] = "unassigned"
                    all_jobs.append(job)
                bundle.data['jobs'] = all_jobs

            except:
                pass

        return self.create_response(request, bundle)
        

    @action(allowed=['get'], require_loggedin=False,static=True)
    def get_all_pending_jobs(self, request, **kwargs):
        self.is_authenticated(request)
       
        bundle = self.build_bundle(data={}, request=request)
        try:
            #bundle = self.build_bundle(data={}, request=request) # we specify the type of bundle in order to help us filter the action we take before we return
            uob = bundle.request.user
            part_of_groups = uob.groups.all()
            perm = Permissions(part_of_groups)
            list_of_company_ids_admin = perm.check_auth_admin()
            list_of_company_ids_tech = perm.check_auth_tech()

            pending_jobs = PendingJobs.objects.filter(technician__user=uob)
            #pdb.set_trace()
            serialized_jobs = json.loads( serializers.serialize('json', pending_jobs) )
            all_jobs = []
            for nn,ii in enumerate(serialized_jobs):
                job = {}
                job['uri'] = '/api/v1/biogasplants/'+str(ii['fields']['biogas_plant']) +'/'
                job['region'] = pending_jobs[nn].biogas_plant.region
                job['district'] = pending_jobs[nn].biogas_plant.district
                job['ward'] = pending_jobs[nn].biogas_plant.ward
                job['volume'] = pending_jobs[nn].biogas_plant.volume_biogas
                job['longitude'] = pending_jobs[nn].biogas_plant.location.get_x()
                job['latitude'] = pending_jobs[nn].biogas_plant.location.get_y()
                job['QP_status'] = pending_jobs[nn].biogas_plant.QP_status
                job['sensor_status'] = pending_jobs[nn].biogas_plant.sensor_status
                job["current_status"] = pending_jobs[nn].biogas_plant.current_status
                install_date = pending_jobs[nn].biogas_plant.install_date
                if install_date is not None:
                     job['install_date']=install_date.strftime("%Y-%m-%d %H:%M:%S")
                job['type_biogas'] = pending_jobs[nn].biogas_plant.type_biogas
                job['uid'] = uuid.UUID(ii['pk']).hex
                job['job_details'] = ii['fields']['job_details']
                job['date_created'] = ii['fields']['datetime_created']
                all_jobs.append(job)
            bundle.data['jobs'] = all_jobs
        except:
            pass

        return self.create_response(request, bundle)

    @action(allowed=['put'], require_loggedin=True)
    def remove_pending_job(self, request, **kwargs):
        self.is_authenticated(request)
        pdb.set_trace()
        pass


    class Meta:
        queryset = PendingJobs.objects.all()
        resource_name = 'pendingjobs'
        excludes = []
        list_allowed_methods = ['get', 'patch','post']
        filtering = {}
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            #post=("read write",),
            get=("read",),
            put=("read","write")
        )

    def dehydrate(self, bundle):
        fields_to_keep = ["biogas_plant","job_id","datetime_created","job_details"]
        bundle = keep_fields(bundle,fields_to_keep)
        return bundle

    def hydrate(self, bundle):
        #BiogasPlant
        #TechnicianDetail
        #pdb.set_trace()
        pass
        return bundle



    def obj_update(self, bundle, **kwargs):
        #pdb.set_trace()
        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        uob = bundle.request.user
        part_of_groups = uob.groups.all()
        perm = Permissions(part_of_groups)
        list_of_company_ids_admin = perm.check_auth_admin()
        list_of_company_ids_tech = perm.check_auth_tech()

        if uob.is_superuser:
            try:
                bundle.obj = PendingJobs.objects.get(pk=pk) # a superuser can edit any technican's record
            except:     
                raise CustomBadRequest(
                        code="403",
                        message="Object not found")
        else:
            flag = 0
            if list_of_company_ids_admin[0] is True: # pk=pk,,
                try:
                    
                    bundle.obj = PendingJobs.objects.get(Q(pk=pk),Q(associated_company__company_id__in = list_of_company_ids_admin[1]) | Q(constructing_technicians__company__company_id__in = list_of_company_ids_admin[1]) ) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['UIC','contact','constructing_technicians','funding_souce','funding_source_notes','country','region','district','ward','village','postcode','other_address_details','type_biogas','supplier','volume_biogas','what3words','location','QP_status','sensor_status','current_status','verfied']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                    flag = 2
                except:
                    flag = 1
                
            elif ( (flag == 1 or flag==0) and list_of_company_ids_tech[0] is True ):
                try:
                    bundle.obj = PendingJobs.objects.get(Q(pk=pk),Q(associated_company__company_id__in = list_of_company_ids_admin[1]) | Q(constructing_technicians__company__company_id__in = list_of_company_ids_admin[1]))
                    #bundle.obj = UserDetail.objects.get(pk=pk,company__company_id__in = list_of_company_ids_tech[1]) # a superuser can edit any technican's record
                    fields_to_allow_update_on = ['UIC','contact','constructing_technicians','funding_souce','funding_source_notes','country','region','district','ward','village','postcode','other_address_details','type_biogas','supplier','volume_biogas','what3words','location','QP_status','sensor_status','current_status','verfied']
                    bundle = keep_fields(bundle, fields_to_allow_update_on)
                except:     
                    raise CustomBadRequest(
                            code="403",
                            message="You do not have permission to edit that contact")
                
            else:
                bundle.obj = BiogasPlant.objects.none()
                bundle.data ={}

        bundle = self.full_hydrate(bundle)

        #pdb.set_trace(0)
        return super(PendingJobsResource, self).obj_update(bundle, user=uob)

    


    def obj_create(self, bundle, **kwargs):
        # only superusers and create and delete pending jobs
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)

        if uob.is_superuser:
            bundle = self.full_hydrate(bundle)
        else:
            bundle.obj = PendingJobs.objects.none()
            bundle.data = []

        

        return super(PendingJobsResource, self).obj_create(bundle) #user=bundle.request.user

    def obj_delete(self, bundle, **kwargs):

        try:
            pk = int(kwargs['pk'])
        except:
            pk = kwargs['pk']

        if uob.is_superuser:
            bundle.obj = PendingJobs.objects.get(pk=pk)
            bundle.obj.delete()
        else:
            bundle = PendingJobs.objects.none() # non-superusers cannot delete objects

        return super(PendingJobsResource, self).obj_delete(bundle, user=uob)



    def authorized_read_list(self, object_list, bundle):
        #return object_list.filter(user=bundle.request.user)
        #pdb.set_trace()
        uob = bundle.request.user
        user_object = UserDetail.objects.filter(user=uob)
        if uob.is_superuser:
            return object_list

        if user_object[0].role.label == 'Company Admin': # return all the people associated with this company
            #pdb.set_trace()
            company_object = user_object[0].company.all()
            company_names = [co.company_name for co in company_object]
            return object_list.filter(Q(contact__associated_company__company_name__in=company_names) | Q(associated_company__company_name__in=company_names))

        if user_object[0].role.label == 'Technician': # only return the user info of the logged in technican
            # a technician cannot get the user details associated with a company
            #pdb.set_trace()
            # we want to filter and return only the biogas plants associated with that technican
            #object_list.biogas_plant_detail
            return []