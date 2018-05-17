from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Card, CardTemplate, CardOrder, PendingAction, \
    UtilisationStatus, TrendChangeDetectionPDecrease, TrendChangeDetectionPIncrease, BiogasSensorStatus, AutoFault, DataConnection, IndictorJoinTable
from tastypie.authorization import DjangoAuthorization
from tastypie_oauth2.authentication import OAuth20Authentication
from tastypie_oauth2.authentication import OAuth2ScopedAuthentication
from tastypie.constants import ALL
from django_dashboard.api.api_biogas_details import BiogasPlantResource
from helpers import Permissions
from helpers import CustomBadRequest
from helpers import keep_fields
import uuid
import traceback
from copy import copy
from tastypie_actions.actions import actionurls, action
from django.core import serializers
import serpy
from django.db.models import Q
import uuid
import json
from helpers import datetime_to_string, error_handle_wrapper, only_keep_fields, map_fields, to_serializable, AddressSerializer
from django.core.paginator import Paginator
from tastypie_actions.actions import actionurls, action
from django_postgres_extensions.models.functions import ArrayAppend, ArrayReplace
from django.contrib.gis.geos import Point
import datetime
import pdb


class DataResource(ModelResource):
    class Meta:
        queryset = Card.objects.all() # everything in the Techicians database - or use Entry.objects.all().filter(pub_date__year=2006) to restrict what is returned
        resource_name = 'data' # when it is called its name will be called technicians
        excludes = []
        list_allowed_methods = ['get', 'post', 'put']
        filtering = {
                    } # can use the filtering options from django
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            post=("read write",),
            get=("read",),
            put=("read", "write"),
            
        )

    def prepend_urls(self):
        return actionurls(self)