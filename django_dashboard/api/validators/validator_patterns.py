from cerberus import Validator
# import phonenumbers
# from phonenumbers import carrier
# from phonenumbers.phonenumberutil import number_type
import pdb
import re

# class SmartBiogasValidator(Validator):
#    def _validate_what3words(self, what3words, field, value):
#         if what3words:
#             pattern = re.compile("^[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+$")
#             valid = bool(pattern.match(value))
            

def what3words_validator(field, value, error):
    if value is None:
        valid = True
    else:
        pattern = re.compile("^[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+$")
        valid = bool(pattern.match(value))
        if not valid:
            error(field, "what3wowrds needs to be 3 strings separated by a '.' e.g. 'apple.french.lovely' ")

def biogas_plant_uri_validator(field, value, error):
    pattern = re.compile("^\/api\/v1\/biogasplants\/[0-9]+\/$")
    valid = bool(pattern.match(value))
    if not valid:
        error(field, "the uri should be of the form: '/api/v1/biogasplants/20/' the final digit should be an int that refers to the specific biogas plant you want to link")

def technician_uri_validator(field, value, error):
    pattern = re.compile("^\/api\/v1\/users\/[0-9]+\/$")
    valid = bool(pattern.match(value))
    if not valid:
        error(field, "the uri should be of the form: '/api/v1/users/10/' the final digit should be an int that refers to the specific user you want to link")

def validate_mobile(field, value, error):
    #pattern = re.compile("^\+[0-9]+$")
    #valid = bool(pattern.match(value))
    pattern = re.compile("^[\+][1-9][0-9]+$")
    isnumber = bool(pattern.match(value))
    #a_mobile = carrier._is_mobile(number_type(phonenumbers.parse(value)))
    if isnumber is False:
        error(field, "This field should contain an phone number in international format, e.g. +457543788853")


schema = {

    "create_technician": {
                            'role': {'type': 'integer', 'allowed': [1, 2]},
                            'first_name':{'type': 'string','required':True},
                            'last_name':{'type': 'string','required':True},
                            #'phone_number':{ 'type': 'string', 'regex':'^\+[0-9]+$'},
                            #'mobile':{ 'type': 'string', 'regex':'^\+[0-9]+$', 'required':True},
                            'phone_number': { 'type':'string', 'validator':validate_mobile },
                            'mobile': { 'type':'string', 'validator':validate_mobile, 'required':True },
                            'email':{'type':'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
                            'country':{'type': 'string','required':True},
                            'region':{'type': 'string','required':True},
                            'postcode':{'type': 'string'},
                            'district':{'type': 'string'},
                            'ward':{'type': 'string'},
                            'village':{'type': 'string'},
                            'other_address_details':{'type': 'string'},
                            'acredit_to_install':{'type': 'list', 'allowed':['tubular','fixed_dome']},
                            'acredited_to_fix':{'type': 'list', 'allowed':['tubular','fixed_dome']},
                            'specialist_skills':{'type': 'list', 'allowed':['plumber','mason','manager','design','calculations']},
                            'status':{'type':'boolean','required':True},
                            'willing_to_travel':{'type': 'integer','min': 0 },
                            'max_num_jobs_allowed':{'type': 'integer', 'max':10},
                            'languages_spoken': {'type': 'list', 'schema': {'type': 'string'} },
                            'user_photo':{'type':'string'},
                            'what3words':{'type': 'string','validator': what3words_validator},
                            'username':{'type':'string', 'required':True, 'required':True},
                            'password':{ 'type':'string', 'required':True, 'minlength':6 },
                        },

    "edit_technician": {
                            'role': {'type': 'integer', 'allowed': [1, 2]},
                            'first_name':{'type': 'string'},
                            'last_name':{'type': 'string'},
                            #'phone_number':{'type': 'string','regex':'^\+[0-9]+$'},
                            #'mobile':{'type': 'string', 'regex':'^\+[0-9]+$'},
                            'email':{'type':'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
                            'phone_number': { 'type':'string', 'validator':validate_mobile },
                            'mobile': { 'type':'string', 'validator':validate_mobile },
                            'country':{'type': 'string'},
                            'region':{'type': 'string'},
                            'district':{'type': 'string'},
                            'ward':{'type': 'string'},
                            'village':{'type': 'string'},
                            'other_address_details':{'type': 'string'},
                            'acredit_to_install':{'type': 'list', 'allowed':['tubular','fixed_dome']},
                            'acredited_to_fix':{'type': 'list', 'allowed':['tubular','fixed_dome']},
                            'specialist_skills':{'type': 'list', 'allowed':['plumber','mason','manager','design','calculations']},
                            'status':{'type':'boolean'},
                            'willing_to_travel':{'type': 'integer','min': 0 },
                            'max_num_jobs_allowed':{'type': 'integer', 'max':10},
                            'languages_spoken': {'type': 'list', 'schema': {'type': 'string'} },
                            'user_photo':{'type':'string'},
                            'what3words':{'type': 'string','validator': what3words_validator},
                            'username':{'type':'string', 'required':True },
                            'password':{ 'type':'string', 'required':True, 'minlength':6 }
                        },

    "create_biogas_contact":{
                            "contact_type":{'type': 'integer', 'allowed': [1, 2, 3, 4]},
                            "firstname":{'type': 'string','required':True},
                            "surname":{'type': 'string','required':True},
                            "mobile":{'type': 'string','regex':'^\+[0-9]+$', 'required':True},
                            "country":{'type': 'string'},
                            "village":{'type': 'string'},
                            "region":{'type': 'string'},
                            "district":{'type': 'string'},
                            "ward":{'type': 'string'},
                            "latitude":{'type':'float'},
                            "longitude":{'type':'float'},
                            "what3words":{'type': 'string','validator': what3words_validator},
                            "UIC":{'type': 'string'}
    },

    "create_biogas_plant":{
                            "UIC":{'type': 'string'}, 
                            "biogas_plant_name":{'type': 'string'},
                            "contact":{'type': 'string'},
                            "funding_source":{'type': 'integer', 'allowed': [1, 2, 3]},
                            "latitude":{'type':'float'},
                            "longitude":{'type':'float'},
                            "what3words":{'type': 'string','validator': what3words_validator},
                            "type_biogas":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5]},
                            "volume_biogas":{'type': 'string', 'allowed': ['<3m3','3m3','4m3','5m3','6m3','7m3','8m3','9m3','10m3','11m3','12m3','>12m3']},
                            "install_date":{'type': 'integer'},
                            "current_status":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5]},
                            "construction_tech":{'type': 'string','allowed':['me','none']},
                            "location_estimated":{'type':'boolean'},
                            "funding_source_notes":{'type': 'string'},
                            "country":{'type': 'string','required':False},
                            "region":{'type': 'string','required':False },
                            "district":{'type': 'string','required':False},
                            "ward":{'type': 'string','required':False},
                            "village":{'type': 'string','required':False},
                            "other_address_details":{ 'type': 'string','required':False },
                            "supplier":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5, 6]},
                            "QP_status":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5, 6, 7]},
                            "sensor_status":{'type': 'integer', 'allowed': [1, 2, 3]},
                            "verfied":{'type':'boolean'},
                            "what3words":{'type': 'string','validator': what3words_validator},
                            "associated_company":{'type': 'string'},
                            },

    "edit_biogas_plant":{
                            "UIC":{'type': 'string'}, 
                            "biogas_plant_name":{'type': 'string'},
                            "contact":{'type': 'string'},
                            "funding_source":{'type': 'integer', 'allowed': [1, 2, 3]},
                            "latitude":{'type':'float'},
                            "longitude":{'type':'float'},
                            "what3words":{ 'validator': what3words_validator },
                            "type_biogas":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5]},
                            "volume_biogas":{'type': 'string', 'allowed': ['<3m3','3m3','4m3','5m3','6m3','7m3','8m3','9m3','10m3','11m3','12m3','>12m3']},
                            "install_date":{'type': 'integer'},
                            "current_status":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5]},
                            "construction_tech":{'type': 'string','allowed':['me','none']},
                            "location_estimated":{ 'type':'boolean', 'required':False },
                            "biogas_plant_name":{'type': 'string'},
                            "funding_source_notes":{'type': 'string'},
                            "country":{'type': 'string','required':False},
                            "region":{'type': 'string','required':False},
                            "district":{'type': 'string','required':False},
                            "ward":{'type': 'string','required':False},
                            "village":{'type': 'string','required':False},
                            "other_address_details":{'type': 'string','required':False},
                            "supplier":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5, 6]},
                            "QP_status":{'type': 'integer', 'allowed': [1, 2, 3, 4, 5, 6, 7]},
                            "sensor_status":{'type': 'integer', 'allowed': [1, 2, 3]},
                            "verfied":{'type':'boolean'},
                            "associated_company":{'type': 'string'},
                            },

    "create_pending_job":{
                            "technician": { 'type': 'string', 'validator': technician_uri_validator },
                            "job_details": {'type': 'string'},
                            "biogas_plant":{ 'type': 'string', 'validator': biogas_plant_uri_validator }
                        },

    "register_node": {
                        "UIC": { 'type': 'string', 'required':True},
                        "channel": {'type': 'integer', 'required':True},
                        "band": {'type': 'integer', 'required':True},
                        "mode": {'type': 'integer', 'required':True},
                        "nw_key": {'type': 'string', 'required':True}

                    },

    "update_card_value": {
                            "template_id": { 'type': 'string', 'required':True },
                            "value": { 'type': 'string', 'required':True }
                        },

    "update_or_add_pending_action": {
                            "template_id": { 'type': 'string', 'required':True },
                            "message": { 'type': 'string', 'required':False },
                            "alert_type":{ 'type': 'string','allowed':['CONTACT', 'EDIT', 'REASSIGN', 'FINDSUPPORT', 'DISPUTE', 'LONGOUTSTANDING', 'POORFEEDBACK', 'NEEDTECHICIAN', 'OTHER', 'INFO'] , 'required':False },
                            "entity_id": { 'type': 'string', 'required':False },
                            "action_url": { 'type': 'string', 'required':False },
                            "action_object": { 'type': 'string', 'required':False }
                                },
    "update_indicators" : {
                        "plant_id": { 'type': 'integer', 'required':True },
                        "type_indicator": { 'type': 'string', 'required':True },
                        "info": { 'type': 'dict', 'required': False },
                        "status": { 'type': 'integer', 'required': True },
                        "value": { 'type': 'string', 'required': False }
                           },               

}