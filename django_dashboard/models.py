# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField, HStoreField, JSONField
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
from geopy.geocoders import Nominatim
from django.utils import timezone
import uuid
from random import randint # for testing data streams
from enumfields import EnumField
from django_dashboard.enums import ContactType, UserRole, JobStatus, QPStatus, CurrentStatus, TypeBiogas, SupplierBiogas, SensorStatus,FundingSourceEnum
from django_dashboard.utilities import find_coordinates
from multiselectfield import MultiSelectField
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

import pdb

#class UserE(models.Model):
#    user = models.OneToOneField(User, related_name='user')




class Company(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #session = models.ForeignKey(Session)
    

    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    company_name = models.CharField(max_length=200)

    country = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    region = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    district = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    ward = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    village = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    postcode = models.CharField(null=True,max_length=20,blank=True)
    neighbourhood = models.CharField(null=True,max_length=20,blank=True)
    other_address_details = models.TextField(null=True,blank=True)
    #phone_number = models.CharField(max_length=15, db_index=True,null=True)
    phone_number = PhoneNumberField(db_index=True, null=True, blank=True)
    emails = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True)
    other_info = models.TextField(blank=True,null=True)

    def __str__(self):
        return '%s' % (self.company_name)

    def save(self, *args, **kwargs):
        self.create_groups(self.company_name,self.company_id)
        return super(Company,self).save(*args,**kwargs)

    def create_groups(self,company_name,company_id):
        """Each company has three groups which can have defined permissions"""
        #pdb.set_trace()
        tech_group_name = slugify(company_name)+"__tech__"+str(self.company_id) # we need to check it does not exist before this step
        admin_group_name = slugify(company_name)+"__admin__"+str(self.company_id)
        superadmin_group_name = slugify(company_name)+"__superadmin__"+str(self.company_id)
        new_group1, created1 = Group.objects.get_or_create(name=tech_group_name)
        new_group2, created2 = Group.objects.get_or_create(name=admin_group_name)
        new_group3, created3 = Group.objects.get_or_create(name=superadmin_group_name)
        # now when a new user is created, we
        #ct = ContentType.objects.get_for_model(User)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company's"
        #ordering =['company_id','company_name','']

    


class UserDetail(models.Model):
    #uid = models.CharField(db_index=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE) # a user
    #admin_role_in_companies = models.ManyToManyField(Company, blank=True, related_name="admin_role_in",) # the companies the User has an admin role in
    #technican_role_in_companies = models.ManyToManyField(Company, blank=True,related_name="tech_role_in") # the companies the User has a technican role in
    
    company = models.ManyToManyField(Company)
    #models.ManyTo.ManyField(Company)
    # maybe add choices here:
    
    role = EnumField(UserRole, max_length=1,null=True)
    #pdb.set_trace()
    first_name = models.CharField(max_length=200,default=None,editable=False)
    last_name = models.CharField(max_length=200,default=None,editable=False)
    #last_name = models.CharField(max_length=200)
    user_photo = models.ImageField(upload_to = 'UserPhotos',null=True,blank=True)
    #phone_number = models.CharField(max_length=15, db_index=True,null=True) # we'll need to add some validaters for this
    phone_number = PhoneNumberField(db_index=True, null=True, blank=True)
    country = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    region = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    #region = models.ManyToManyField('django_dashboard.region')
    district = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    ward = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    village = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    neighbourhood = models.CharField(null=True,max_length=20,blank=True)
    postcode = models.CharField(null=True,max_length=20,blank=True)
    postcode = models.CharField(null=True,max_length=20,blank=True)
    other_address_details = models.TextField(null=True,blank=True)
    datetime_created = models.DateTimeField(editable=False, db_index=True,null=True,blank=True)
    datetime_modified = models.DateTimeField(null=True,blank=True,editable=False)

    def __str__(self):
        return '%s, %s %s' % (self.last_name,self.first_name,self.phone_number)

    def save(self, *args, **kwargs):
        self.add_new_users_to_groups()
        if not self.datetime_created:
            self.datetime_created = timezone.now()
        self.datetime_modified = timezone.now()
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name


        #pdb.set_trace()
        #pdb.set_trace()
        return super(UserDetail,self).save(*args,**kwargs)
    
    def add_new_users_to_groups(self): # initially add the users to the technican's group of the company that they are in
        #pdb.set_trace()
        companies = self.company.all()
        for cy in companies:
            tech_group_name = slugify(cy.company_name)+"__tech__"+str(cy.company_id)
            _group_, created = Group.objects.get_or_create(name=tech_group_name)
            _group_.user_set.add(self.user)


        #new_group2, created2 = Group.objects.get_or_create(name=admin_group_name)
        #new_group3, created3 = Group.objects.get_or_create(name=superadmin_group_name)

    def company_title(self):
        #pdb.set_trace()
        self.company_query_object = self.company.all()
        return "\n".join([p.company_name for p in self.company_query_object])

    company_title.short_description = 'Company Name'
    company_title.allow_tags = True

    class Meta:
        verbose_name = "UserDetail"
        verbose_name_plural = "UserDetails"
        permissions = ( ("remove_user", "Remove a user from the platform"),
                        ("create_user", "Add a user to the platform" ),
                        ("edit_user", "Edit a user's profile"),

        )

class TechnicianDetail(models.Model):
    BOOL_CHOICES = ((True, 'Active'), (False, 'Inactive'))

    ACCREDITED_TO_INSTALL = (
    ('TUBULAR', "tubular"),
    ('FIXED_DOME', "fixed_dome"),
    )

    SPECIALIST_SKILLS = (
        ('PLUMBER', 'plumber'),
        ('MASON', 'mason'),
        ('MANAGER', 'manager'),
        ('DESIGN', 'design'),
        ('CALCULATIONS', 'calculations')
    )

    #tech = models.ForeignKey(Technicians, on_delete=models.CASCADE)
    technicians = models.OneToOneField(
        UserDetail,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="technician_details",
    )
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    technician_id = models.UUIDField(default=uuid.uuid4, editable=False,db_index=True)
    #acredit_to_install = ArrayField(models.CharField(max_length=200, choices = ACCREDITED_TO_INSTALL), default=list,blank=True, db_index=True,null=True) # choices=ACCREDITED_TO_INSTALL e.g. different digesters they can construct
    #acredit_to_install = models.SelectMultiple(max_length=200, choices = ACCREDITED_TO_INSTALL)
    acredit_to_install = MultiSelectField(choices = ACCREDITED_TO_INSTALL,blank=True, db_index=True,null=True)
    acredited_to_fix = MultiSelectField(choices = ACCREDITED_TO_INSTALL,blank=True, db_index=True,null=True)
    #acredited_to_fix = ArrayField(models.CharField(max_length=200), default=list, blank=True, db_index=True,null=True)
    specialist_skills = MultiSelectField(choices = SPECIALIST_SKILLS,blank=True, db_index=True,null=True)
    #specialist_skills = ArrayField(models.CharField(max_length=200), default=list, blank=True, db_index=True,null=True)
    number_jobs_active = models.IntegerField(blank=True,null=True)
    number_of_jobs_completed = models.IntegerField(blank=True,null=True)
    #seconds_active = models.IntegerField(blank=True,null=True)
    status = models.NullBooleanField(db_index=True,blank=True,null=True,choices=BOOL_CHOICES)
    what3words = models.CharField(max_length=200,null=True)
    location = models.PointField(geography=True, srid=4326,blank=True,null=True,db_index=True)
    willing_to_travel = models.IntegerField(blank=True,null=True) # distance that a technician is willing to travel
    #rating = ArrayField(JSONField(blank=True, null=True),blank=True, null=True )
    average_rating = models.FloatField(editable=False,blank=True,null=True,default=0)
    max_num_jobs_allowed = models.IntegerField(blank=True,null=True,default=1)
    languages_spoken = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True)
    
    
    def __str__(self):
        return '%s %s' % (self.technicians,self.status)

    def update_location(self,lat_,long_):
        self.location = Point(long_, lat_)
        self.save()
    
    def update_status(self,status):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        if  (self.what3words != None): # want to change this so it is only saved when the coordinate has changed, not every time
            _location_ = find_coordinates(self.what3words)
            self.location = Point( _location_['lng'], _location_['lat'] )
        return super(TechnicianDetail,self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Status and Location"
        verbose_name_plural = "Status and Location"

        permissions = ( ("remove_technician", "Remove a technician from the platform"),
                        ("create_technician", "Add a technician to the platform" ),
                        ("edit_technician", "Edit a technican's profile"),

        )

class BiogasPlantContact(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    #associated_company = models.ManyToManyField(Company)
    associated_company = models.ForeignKey(Company, on_delete=models.CASCADE ) # this field will be depreciated in the production version as will be on the biogas plant instead (and will be the company who constructed)
    contact_type = EnumField(ContactType, max_length=1)
    first_name = models.CharField(null=True,max_length=200)
    surname = models.CharField(null=True,max_length=200)
    mobile = models.CharField(db_index=True,null=True,blank=True,max_length=15)
    email = models.CharField(validators=[EmailValidator],db_index=True,null=True,blank=True,max_length=200)
    # biogas_owner = models.NullBooleanField(db_index=True,blank=True)


    def __str__(self):
        return '%s %s; %s' % (self.first_name, self.surname, self.mobile)

    class Meta:
        verbose_name = "Biogas Plant Owner"
        verbose_name_plural = "Biogas Plant Owners"

        permissions = ( ("remove_user", "Remove a user from the platform"),
                        ("create_user", "Add a user to the platform" ),
                        ("edit_user", "Edit a user's profile"),
                        ("edit_mobile_number","Able to Edit a users mobile number")

        )
    
class BiogasPlant(models.Model):
    TYPE_BIOGAS_CHOICES = (
    ('TUBULAR', "tubular"),
    ('FIXED_DOME', "fixed_dome"),
    ('GESISHAMBA','GesiShamba'),
    )

    STATUS_CHOICES = (
        ('UNDER_CONSTRUCTION', 'under construction'),
        ('COMMISSIONING', 'commissioning'),
        ('QP1_operational','QP1 operational'),
        ('QP1_fault','QP1 fault'),
        ('QP2_operational','QP2 operational'),
        ('QP2_fault','QP2 fault'),
        ('OPERATIONAL','operational'),
        ('FAULT','fault'),
        ('DECOMMISSIONED', "decommissioned"),
    )
    plant_id = models.UUIDField(default=uuid.uuid4, editable=False,db_index=True)
    
    UIC = models.CharField(db_index=True,null=True,blank=True,max_length=200) # Unique Identiifer Code (their is one of these on all biogas plants)
    biogas_plant_name = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    
    associated_company = models.ManyToManyField(Company, blank=True, related_name='biogas_plant_company') 
    contact = models.ManyToManyField(BiogasPlantContact, related_name='biogas_plant_detail') # a biogas plant can have one or many users and a user can have one or many biogas plants
    constructing_technicians = models.ManyToManyField(UserDetail,blank=True, related_name = 'constructing_technicians')

    funding_souce = EnumField(FundingSourceEnum, max_length=1,null=True, blank = True)
    funding_source_notes = models.TextField(null=True, blank=True)
    
    country = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    region = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    district = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    ward = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    village = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    postcode = models.CharField(null=True,max_length=20,blank=True)
    neighbourhood = models.CharField(null=True,max_length=20,blank=True)
    other_address_details = models.TextField(null=True,blank=True)
    #type_biogas = models.CharField(choices=TYPE_BIOGAS_CHOICES,null=True,max_length=20,blank=True)
    type_biogas = EnumField(TypeBiogas, max_length=1,null=True)
    supplier = EnumField(SupplierBiogas, max_length=1,null=True,blank=True)
    #size_biogas = models.FloatField(null=True,blank=True) # maybe specify this in m3
    volume_biogas = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    volume_biogas = models.CharField(max_length=200,null=True,blank=True)
    location = models.PointField(geography=True, srid=4326,blank=True,db_index=True,null=True)
    #status = models.CharField(null=True,max_length=225,blank=True,choices=STATUS_CHOICES)
    QP_status = EnumField(QPStatus, max_length=1,null=True)
    sensor_status = EnumField(SensorStatus, max_length=1,null=True, blank = True)
    current_status = EnumField(CurrentStatus, max_length=1,null=True)
    verfied = models.NullBooleanField(db_index=True,blank=True,default=False)
    install_date = models.DateField(null=True,blank=True)


    def __str__(self):
        return '%s, %s, %s, %s' % (str(self.type_biogas), str(self.supplier), str(self.volume_biogas), str(self.plant_id) )

    def get_contact(self):
        #pdb.set_trace()
        self.contact_query_object = self.contact.all()
        return "\n".join([p.surname+", "+p.first_name for p in self.contact_query_object])
    get_contact.short_description = 'Contact'
    get_contact.allow_tags = True

    def mobile_num(self):
        #pdb.set_trace()
        return "\n".join([p.mobile for p in self.contact_query_object])

    mobile_num.short_description = 'Mobile'
    mobile_num.allow_tags = True

    def contact_type(self):
        #pdb.set_trace()
        return "\n".join([p.contact_type.name for p in self.contact_query_object])

    contact_type.short_description = 'Type'
    contact_type.allow_tags = True

    def save(self, *args, **kwargs):
        #if not self.location:
        #    geolocator = Nominatim()
        #   _location_ = geolocator.geocode(self.town)
        #    self.location = Point(_location_.longitude, _location_.latitude)
        if  (self.what3words != None): # want to change this so it is only saved when the coordinate has changed, not every time
            _location_ = find_coordinates(self.what3words)
            self.location = Point( _location_['lng'], _location_['lat'] )
        return super(BiogasPlant, self).save(*args, **kwargs)

        

    class Meta:
        verbose_name = "Biogas Plant"
        verbose_name_plural = "Biogas Plants"

        permissions = ( ("remove_biogas", "Remove a biogas plant from the platform"),
                        ("create_biogas", "Add a biogas plant to the platform" ),
                        ("edit_biogas", "Edit a biogas plant profile"),
                        ("edit_location_biogas","Able to edit a location associated with a biogas plant")

        )

# have an array of fault types
class JobHistory(models.Model):
    plant = models.ForeignKey(BiogasPlant, on_delete=models.CASCADE) # a biogas plan can have many job records
    fixers = models.ManyToManyField(UserDetail,blank=True) # associating it with someone who can fix it, blank means it is optional  - importan because it will not initially be associated
    accepted_but_did_not_visit = models.ManyToManyField(UserDetail,blank=True, related_name='acceptednovisit')
    rejected_job = models.ManyToManyField(UserDetail,blank=True, related_name='rejectedjob')
    rejected_jobs = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True)
    
    STATUS_CHOICES = (
    ('UNASSIGNED', "unassigned"),
    ('RESOLVING', "resolving"),
    ('ASSISTANCE', "assistance"),
    ('OVERDUE', "overdue"),
    ('DECOMMISSIONED', "decommissioned"),
)
    FAULT_CLASSES = (
        ('MINOR', "minor"),
        ('MAJOR', "major"),
    )
    # one to one to relationship
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    #technicians_ids = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True) # a list of the technicians workng on this biogas
    date_flagged = models.DateTimeField(null=True)
    date_accepted = models.DateTimeField(editable=False, db_index=True,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)# when the job should be completed by, this could be based on the problem e.g. water in the pipe would be less than rebuilding the plant
    #job_duration = models.IntegerField() # how long the job has been outstanding in seconds
    date_completed = models.DateField(null=True,blank=True)
    completed = models.NullBooleanField(db_index=True,blank=True,default=False)
    #job_status = models.CharField(choices=STATUS_CHOICES,default='UNASSIGNED',max_length=16,null=True)# states (unassigned, resolving- being worked on, assitance, overdue- accepted, but not been completed, after x number of days, resolved, feedback- if received low star, then flag up and push to an admin)
                # decommissioned
    dispute_raised = models.NullBooleanField(default=False,blank=True)
    job_status= EnumField(JobStatus, max_length=1,null=True)
    verification_of_engagement = models.NullBooleanField(db_index=True,blank=True,default=False)
    fault_description = models.TextField(null=True,blank=True) # a descrete number of fault descriptions
    other = models.TextField(null=True,blank=True) # another unspecified fault description
    client_feedback_star = models.IntegerField(
        default=None,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
     )
    
    client_feedback_additional = models.TextField(null=True,blank=True)# if the customer wants to give additional feedback
  
    overdue_for_acceptance = models.NullBooleanField(default=False,blank=True)# true or false - if after a certain period the job has not been accepted, mark as overdue and then flag priority
    priority = models.NullBooleanField(default=False,blank=True) # this can be triggered manually - increases search radius + confirm if techcians ara able to do or not
    fault_class = models.CharField(null=True,max_length=225,blank=True,choices=FAULT_CLASSES)
    assistance = models.NullBooleanField(default=False,blank=True)
    description_help_need = models.TextField(null=True,blank=True)
    reason_abandoning_job = models.TextField(null=True,blank=True)

    @property
    def _completed(self):
        return self.completed
        
    @_completed.setter
    def set_completed(self,value):
        pdb.set_trace()
        self._complete_signal = True
        self.completed = value
        if (self.completed == True and self.date_completed == None):
            self.date_completed = datetime.datetime.utcnow()
            self.job_status = 4 #'RESOLVED'
        if (self.completed == False and self.date_completed is not None):
            self.date_completed = None
            self.job_status = 2 #'RESOLVING'


    @property
    def _priority(self):
        return self.priority

    @_priority.setter
    def _priority(self,value):
        self.priority = value
        self._priority_signal = True
        if (value == True and self.completed !=True):
            self.job_status = 5 #'FLAG'
        elif (value == False and self.completed !=True):
            self.job_status = 2 #'RESOLVING'
        elif self.completed == True:
            self.job_status = 4 #'RESOLVED'

    @property
    def _assistance(self):
        return self.assistance

    @_assistance.setter
    def _assistance(self,value):
        self._assistance_signal = True
        self.assistance = value
        if (value == True and self.completed !=True):
            self.job_status = 3 #'ASSISTANCE'
        elif (value == False and self._completed !=True):
            self.job_status = 2 #'RESOLVING'
        elif self.completed == True:
            self.job_status = 4 #'RESOLVED'
            


    def save(self, *args, **kwargs):
        #if getattr(self, '_assistance_signal', True): # these can be useful
        #if getattr(self, '_complete_signal', True):
        #if getattr(self, '_priority_signal', True):
        #pdb.set_trace()
        if self.completed is not None:
            self._complete=self.completed
        if self.assistance is not None:
            self._assistance=self.assistance
        if self.priority is not None:
            self._priority=self.priority

        if not self.date_flagged: # when you save it for the first time, make sure we have a time!
            self.date_flagged = timezone.now()

        # use signals to trigger a message to be sent to users once marked
        
        #if __name__ == '__main__':
           
        
       # if __name__ == '__main__':
        #    main()
        return super(JobHistory,self).save(*args,**kwargs)



    class Meta: # we can overide these in the search in the views
       # if (self.priority is False):
          # get_latest_by = ["due_date"] # newest first
        #else:
        get_latest_by = ['-priority', '-date_flagged', ] # True values will come first, with the oldest ones first
        verbose_name = "Job History"
        verbose_name_plural = "Job History"

        permissions = ( ("remove_job", "Remove a job from the platform"),
                        ("create_job", "Add a job to the platform" ),
                        ("edit_job", "Edit a job profile"),
                        ("edit_job_status","Able to edit a job status")

        )

# class AggregatedStatistics(models.Model):
#     plant_type
#     volume
#     funding_souce
#     region
#     supplier
#     number_installed
#     number_commissioning
#     number_commissioned_active
#     number_minor_faults
#     number_major_faults
#     minor_faults_fixed
#     major_faults_fixed
#     ongoing_jobs
#     unrepairable_plants
#     average_repair_time_minor_faults
#     average_repair_time_major_faults
#     datetime

class Dashboard(models.Model):
    #company = models.OneToOneField(Company,on_delete=models.CASCADE, primary_key=True)
    #id = models.BigIntegerField(primary_key = True,default=1)
    company = models.ForeignKey(Company, null=True,on_delete=models.CASCADE) # we want to be able to have many records - and we will display the latest one
    #data_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False, db_index=True)
    
    plants = models.IntegerField(blank=True,null=True)
    active = models.IntegerField(blank=True,null=True)
    faults = models.IntegerField(blank=True,null=True)
    avtime = models.IntegerField(blank=True,null=True)
    jobs = models.IntegerField(blank=True,null=True)
    fixed = models.IntegerField(blank=True,null=True)

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard Data"
        

class AggregatedStatistics(models.Model):
    pass

    def get_data(self):
        data = {'plants':randint(0,100),
            'active':randint(0,100),
            'faults':randint(0,100),
            'avtime':randint(0,100),
            'jobs':randint(0,100),
            'fixed':randint(0,100),
         }
        return data

class AddressData(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    id = models.IntegerField(blank=True,null=True)
    country = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    continent = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    region = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    district = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    ward = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    village = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    lat_long = models.PointField(geography=True, srid=4326,blank=True,null=True,db_index=True)
    population = models.IntegerField(blank=True,null=True)

    #def __str__(self):
       # unicode(self.region)
   #     '%s, %s' % (self.ward, self.village)


class Messages(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    related_job = models.ForeignKey(JobHistory, on_delete=models.CASCADE)
    user_from = models.ForeignKey(User, blank =True, null=True, on_delete=models.CASCADE,related_name="user_from") # so a given user can be associated with a message - we can add this automatically when when a message is sent
    user_to = models.ForeignKey(User, blank =True, null=True, on_delete=models.CASCADE,related_name="user_to") # having these references enables looking up data to be easy for a given user
    message = models.TextField(null=True,blank=True)
    message_type = models.CharField(db_index=True,null=True,blank=True,max_length=30)
    message_id = models.CharField(db_index=True,null=True,blank=True,max_length=200)
    message_from_num = PhoneNumberField(db_index=True,null=True,blank=True)
    message_to_num = PhoneNumberField(db_index=True,null=True,blank=True)
    message_from_email = models.EmailField(null=True,blank=True)
    message_to_email = models.EmailField(null=True,blank=True)


class PendingJobs(models.Model):
    #uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    job_id = models.CharField(db_index=True,default=uuid.uuid4,blank=True,max_length=200, primary_key=True)
    biogas_plant = models.ForeignKey(BiogasPlant, on_delete=models.CASCADE, blank=True, null=True,related_name='abiogasplant') # a job is associated with a biogas plant
    technician = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True,related_name='atechician') # one techncian can have more than one job
    datetime_created = models.DateTimeField(editable=False, db_index=True,null=True,blank=True)
    job_details = models.TextField(null=True,blank=True)
    accepted = models.NullBooleanField(db_index=True,blank=True,null=True,default=None)
    technicians_rejected = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True)
    
    # technicians_rejected will be a list of id's of technicans who have said they do not want this job - the system can get this and use to make sure it does not send messages to these technicians again

    def check_to_accept_job(self):
        if self.accepted is True:
            job_id_uid = uuid(self.job_id) # keep the same id all the way through - makes searching easier!
            JobHistory.objects.create(
                    plant=self.biogas_plant,
                    fixers=technician, 
                    date_flagged=self.datetime_created,
                    job_status=2,
                    fault_description=self.job_details,
                    job_id = job_id_uid
                ) # job_status = 2 means 'resolving'
            # remove job from pending jobs
            PendingJobs.objects.filter(pk=self.id).delete() # delete the pending job
            # now update the technicians details
            techn = TechnicianDetail.objects.filter(technicians=technician)
            techn.number_jobs_active = techn.number_jobs_active + 1 # we'll do this for the time being, in the future might be best to get all the jobs associated with this technician and count up
            techn.status = True # check this is set to true
            # now send message to user to confirm that a technician has accepted
        elif self.accepted is False:
            self.technicians_rejected.append(str(techn.technician_id))
            # now call another function to search for another technician
            

    def save(self, *args, **kwargs):
        self.check_to_accept_job() # check if technician has accepted and then creates a new job for that plant and technician
        
        if not self.datetime_created:
            self.datetime_created = timezone.now()
       

        return super(PendingJobs,self).save(*args,**kwargs)

    
    class Meta: # we can overide these in the search in the views
       # if (self.priority is False):
          # get_latest_by = ["due_date"] # newest first
        #else:
        verbose_name = "Pending Job"
        verbose_name_plural = "Pending Jobs"