from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource , ALL_WITH_RELATIONS
from tastypie import fields, utils
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, PasswordManagement
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
from helpers import datetime_to_string, error_handle_wrapper, only_keep_fields, map_fields
from django.core.paginator import Paginator
from tastypie_actions.actions import actionurls, action
from django_postgres_extensions.models.functions import ArrayAppend, ArrayReplace
from django.contrib.gis.geos import Point
from django.core.mail import send_mail
import datetime
import jwt
from django.conf import settings
import time
import phonenumbers
import hashids
import uuid
import pyaes
import random
import urllib2
import base64
import ConfigParser

BASE_DIR = settings.BASE_DIR

Config = ConfigParser.ConfigParser() # we store security setting in another file
Config.read(BASE_DIR+'/config/configs.ini')
salt = Config.get('password_reset','salt')
expire_in = int(Config.get('password_reset','expire_in'))
encrypt_key = Config.get('password_reset','encryption')

import pdb


class PasswordManagementResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'pass'
        excludes = ['email', 'password', 'is_superuser']
        list_allowed_methods = []
        authorization = DjangoAuthorization()
        authentication = OAuth2ScopedAuthentication(
            #post=("read write",),
            #get=("read",),
            #put=("read", "write"),
        )

    def prepend_urls(self):
        return actionurls(self)

    @action(allowed=['post'], require_loggedin=False, static=True)
    def get_reset_code(self, request, **kwargs):
        #self.is_authenticated(request)
        
        data = json.loads( request.read() )
        fields = ["mobile","email"]
        data = only_keep_fields(data, fields)

        bundle = self.build_bundle(data={}, request=request)
        flag = 0
        try:
            number_object = phonenumbers.parse(data['mobile'], None)
            mobile_sent = phonenumbers.format_number(number_object, phonenumbers.PhoneNumberFormat.INTERNATIONAL).replace(" ", "")
            flag = 0
        except:
            flag = 1
            bundle.data = { "error":"mobile number needs to be in international format" }
            
        #uob = bundle.request.user
        user_object = UserDetail.objects.filter(phone_number=mobile_sent)
        if (flag==0 and (len(user_object)>0) ): # if this is true the user exist in the database
            uob = user_object[0].user
            #pdb.set_trace()
            # we need to just run a loop around this to make sure we never get a repeat
            unique=False
            while unique==False:
                hash_obj  = hashids.Hashids(salt=uuid.uuid4().get_hex())
                hid = hash_obj.encode(random.randint(0,99),random.randint(0,99))
                objs=PasswordManagement.objects.filter(reset_code=hid) # just check the database to make sure
                if len(objs)==0:
                    unique=True
            pm=PasswordManagement()
            pm.reset_code = hid
            pm.expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=20*60)
            pm.user = uob
            pm.save()
            bundle.data = {"message":"If your number exists in the system you will soon receive a message"}
            #pdb.set_trace()
            send_mail('Smart Biogas Password Reset', 'Here is your reset code: '+ str(hid), 'hello@smartbiogas.net', ['diego@ecm.im','joel@creativenergie.co.uk'], fail_silently=False, )   
        return self.create_response(request, bundle)
        
        
        # generate a hashid using random salt + username + mobile number
        # + random 4 digit number

    @action(allowed=['post'], require_loggedin=False, static=True)
    def validate_code(self, request, **kwargs):
        #self.is_authenticated(request)
        data = json.loads( request.read() )
        fields = ["reset_code"]
        time_now = datetime.datetime.now()
        data = only_keep_fields(data, fields)
        # remove all expired codes at this point 
        PasswordManagement.objects.filter(expiry_datetime__lt=time_now).delete()

        code = PasswordManagement.objects.filter(expiry_datetime__gt=time_now,reset_code=data["reset_code"])
        # if the code is correct then reply with the time limited jwt token
        bundle = self.build_bundle(data={}, request=request)
        if (len(code)>0):
            user = code[0].user
            user_name = user.username
            password_hash = user.password
            payload = {'username':user_name, 'hash':password_hash,'expire_at': (time.time() + expire_in)}
            encoded_jwt = jwt.encode(payload, salt, algorithm='HS256')
            aes = pyaes.AESModeOfOperationCTR(encrypt_key)
            cipher_jwt = aes.encrypt(encoded_jwt)
            #bundle.data['token'] = urllib2.quote(encoded_jwt) #base64.urlsafe_b64encode(...)
            bundle.data['token'] = base64.b64encode(cipher_jwt)
            code[0].delete()
        else:
            bundle.data['message'] = "Invalid Code"
            
        return self.create_response(request, bundle)

        # docs on sending emails with django: https://docs.djangoproject.com/en/2.0/topics/email/
        # if code is correct send an email

    @action(allowed=['post'], require_loggedin=False, static=True)
    def reset_password(self, request, **kwargs):
        #self.is_authenticated(request)
        #pdb.set_trace()
        data = json.loads( request.read() )
        fields = ["password","token"]
        data = only_keep_fields(data, fields)

        #try:
        #    st = int(kwargs['pk'])
            #job_id = 
        #except:
        #    st = kwargs['pk']
        st = data["token"]
        #st = urllib2.unquote(st)
        st = base64.b64decode(st)
        aes = pyaes.AESModeOfOperationCTR(encrypt_key)
        decrypted_jwt = aes.decrypt(st)
        try:
            bundle = self.build_bundle(data={}, request=request)
            payload_jwt = jwt.decode(decrypted_jwt, salt, algorithms=['HS256'])
            time_now = time.time()
            uob = User.objects.get(username = payload_jwt['username'])
            old_hash = uob.password
            if ( (time_now<payload_jwt['expire_at']) and payload_jwt['hash']==old_hash ): # if the hash has changes this token has been used before
                uob.set_password(data["password"])
                uob.save()
                bundle.data["message"] = "Password Reset"
            else:
                bundle.data["error"] = "Invalid Token"
        except:
            bundle.data["error"] = "Invalid Token"

        return self.create_response(request, bundle)
        


