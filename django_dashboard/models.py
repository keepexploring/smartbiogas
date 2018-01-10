# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
from geopy.geocoders import Nominatim
from django.utils import timezone
import uuid
from random import randint # for testing data streams

class Company(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    company_name = models.CharField(max_length=200)
    company_address1 = models.CharField(max_length=200)
    company_address2 = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, db_index=True,null=True)
    emails = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True)
    other_info = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company's"

class Technicians(models.Model):
    #uid = models.CharField(db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # maybe add choices here:
    ACCREDITED_TO_INSTALL = (
    ('TUBULAR', "tubular"),
    ('FIXED_DOME', "fixed_dome"),
    )
    technician_id = models.UUIDField(default=uuid.uuid4, editable=False,db_index=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, db_index=True,null=True) # we'll need to add some validaters for this
    nearest_town = models.CharField(db_index=True,null=True,blank=True,max_length=200) # this also needs to be validated, perhaps do on the frontend
    acredit_to_install = ArrayField(models.CharField(max_length=200), default=list,blank=True, db_index=True,null=True) # choices=ACCREDITED_TO_INSTALL e.g. different digesters they can construct
    acredited_to_fix = ArrayField(models.CharField(max_length=200), default=list, blank=True, db_index=True,null=True)
    specialist_skills = ArrayField(models.CharField(max_length=200), default=list, blank=True, db_index=True,null=True)
    datetime_created = models.DateTimeField(editable=False, db_index=True,null=True,blank=True)
    datetime_modified = models.DateTimeField(null=True,blank=True,editable=False)
    average_rating = models.FloatField(editable=False,blank=True,null=True,default=0)

    def save(self, *args, **kwargs):
        if not self.datetime_created:
            self.datetime_created = timezone.now()
        self.datetime_modified = timezone.now()
        return super(Technicians,self).save(*args,**kwargs)

    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"
        permissions = ( ("remove_technician", "Remove a technician from the platform"),
                        ("create_technician", "Add a technician to the platform" ),
                        ("edit_technician", "Edit a technican's profile"),

        )

class TechnitionRealtime(models.Model):
    BOOL_CHOICES = ((True, 'Active'), (False, 'Inactive'))

    #tech = models.ForeignKey(Technicians, on_delete=models.CASCADE)
    technicians = models.OneToOneField(
        Technicians,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    number_jobs_active = models.IntegerField(blank=True,null=True)
    number_of_jobs_completed = models.IntegerField(blank=True,null=True)
    #seconds_active = models.IntegerField(blank=True,null=True)
    status = models.NullBooleanField(db_index=True,blank=True,null=True,choices=BOOL_CHOICES)
    location = models.PointField(geography=True, srid=4326,blank=True,null=True,db_index=True)
    
    def __str__(self):
        return '%s %s' % (self.technicians,self.status)

    def update_location(self,lat_,long_):
        self.location = Point(long_, lat_)
        self.save()
    
    def update_status(self,status):
        self.status = status
        self.save() 

    class Meta:
        verbose_name = "Status and Location"
        verbose_name_plural = "Status and Location"

        permissions = ( ("remove_technician", "Remove a technician from the platform"),
                        ("create_technician", "Add a technician to the platform" ),
                        ("edit_technician", "Edit a technican's profile"),

        )

class Users(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(null=True,blank=True,max_length=200)
    surname = models.CharField(null=True,blank=True,max_length=200)
    mobile = models.CharField(db_index=True,null=True,blank=True,max_length=15)
    email = models.CharField(validators=[EmailValidator],db_index=True,null=True,blank=True,max_length=200)
    biogas_owner = models.NullBooleanField(db_index=True,blank=True)

    
    def __str__(self):
        return '%s %s; %s' % (self.first_name, self.surname, self.mobile)

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"

        permissions = ( ("remove_user", "Remove a user from the platform"),
                        ("create_user", "Add a user to the platform" ),
                        ("edit_user", "Edit a user's profile"),
                        ("edit_mobile_number","Able to Edit a users mobile number")

        )
    
class BiogasPlants(models.Model):
    TYPE_BIOGAS_CHOICES = (
    ('TUBULAR', "tubular"),
    ('FIXED_DOME', "fixed_dome"),
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
    plant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    user = models.ManyToManyField(Users) # a biogas plant can have one or many users and a user can have one or many biogas plants
    town = models.CharField(null=True,max_length=200)
    funding_souce = models.CharField(null=True,max_length=225,blank=True)
    description_location = models.CharField(null=True,max_length=400,blank=True)
    postcode = models.CharField(null=True,max_length=20,blank=True)
    type_biogas = models.CharField(choices=TYPE_BIOGAS_CHOICES,null=True,max_length=20,blank=True)
    size_biogas = models.FloatField(null=True,blank=True) # maybe specify this in m3
    location = models.PointField(geography=True, srid=4326,blank=True,db_index=True,null=True)
    status = models.CharField(null=True,max_length=225,blank=True,choices=STATUS_CHOICES)
    

    def save(self, *args, **kwargs):
        if not self.location:
            geolocator = Nominatim()
            _location_ = geolocator.geocode(self.town)
            self.location = Point(_location_.longitude, _location_.latitude)

        super(BiogasPlants, self).save(*args, **kwargs)

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
    plant = models.ForeignKey(BiogasPlants, on_delete=models.CASCADE) # a biogas plan can have many job records

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
    technicians_ids = ArrayField(models.CharField(max_length=200),default=list, blank=True,null=True) # a list of the technicians workng on this biogas
    date_flagged = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)# when the job should be completed by, this could be based on the problem e.g. water in the pipe would be less than rebuilding the plant
    #job_duration = models.IntegerField() # how long the job has been outstanding in seconds
    date_completed = models.DateTimeField(null=True)
    completed = models.NullBooleanField(db_index=True,blank=True,default=False)
    job_status = models.CharField(choices=STATUS_CHOICES,default='UNASSIGNED',max_length=16,null=True)# states (unassigned, resolving- being worked on, assitance, overdue- accepted, but not been completed, after x number of days, resolved, feedback- if received low star, then flag up and push to an admin)
                # decommissioned
    
    fault_description = models.TextField(null=True) # a descrete number of fault descriptions
    other = models.TextField(null=True) # another unspecified fault description
    client_feedback_star = models.IntegerField(
        default=None,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
        null=True,
     )#
    client_feedback_additional = models.TextField(null=True)# if the customer wants to give additional feedback
  
    overdue_for_acceptance = models.NullBooleanField(default=False)# true or false - if after a certain period the job has not been accepted, mark as overdue and then flag priority
    priority = models.NullBooleanField(default=False) # this can be triggered manually - increases search radius + confirm if techcians ara able to do or not
    fault_class = models.CharField(null=True,max_length=225,blank=True,choices=FAULT_CLASSES)
    #
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
    dash_id = models.OneToOneField(Company,on_delete=models.CASCADE, primary_key=True)
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
