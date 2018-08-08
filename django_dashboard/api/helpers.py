import json

from tastypie.exceptions import TastypieError
from tastypie.http import HttpBadRequest
from django.http import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse
import attr
import datetime
from enumfields import Enum
from django.contrib.gis.geos import Point
import uuid
import serpy
from cerberus import Validator
from django_dashboard.api.validators.validator_patterns import schema
from django.core.exceptions import ObjectDoesNotExist
import uuid
import pdb


class CustomBadRequest(TastypieError):
    """
    This exception is used to interrupt the flow of processing to immediately
    return a custom HttpResponse.
    """

    def __init__(self, code="", message=""):
        self._response = {
            "error": {"code": code or "not_provided",
                      "message": message or "No error message was provided."}}

    @property
    def response(self):
        return HttpBadRequest(
            json.dumps(self._response),
            content_type='application/json')



def raise_custom_error(dict_response,status_code):
    raise ImmediateHttpResponse(response=HttpResponse(json.dumps(dict_response), status=status_code, content_type="application/json"))


def extract_company_id(group_name):
    split_string = group_name.split('__')
    slugified_name = split_string[0]
    permission = split_string[1]
    company_id = split_string[2]
    return {"name": slugified_name, "permissions":[permission], "company_id":company_id }

def check_if_exists(data_list,id_):
    for en,kk in enumerate(data_list):
        if kk["company_id"] == id_:
            return [True, kk["company_id"],en]
    return [False]
from django_dashboard.models import Company
class Permissions():
    
    def __init__(self, uob):
        self.uob = uob
        self.part_of_groups = self.uob.groups.all()
        self._get_roles_and_scope()

    def get_companies_and_permissions(self):
        self.companies_and_permissions = []
        for ii in self.part_of_group:
            try:
                data = extract_company_id(ii.name)
                exists = check_if_exists(self.companies_and_permissions,data["company_id"])
                if (exists[0]==True):
                    self.companies_and_permissions[exists[2]]["permissions"] =  self.companies_and_permissions[exists[2]]["permissions"] + data["permissions"]
                else:
                    self.companies_and_permissions.append(data)
            except:
                pass

        return self.companies_and_permissions

    def _get_roles_and_scope(self):
        roles_and_scope = {}
        roles_and_scope['logged_in_as'] = []
        roles_and_scope['other_roles'] = []
        
        try:
            self.logged_in_as_company = self.uob.userdetail.logged_in_as
            
            if self.logged_in_as_company is None: # this is to ensure backwards compatability with existing users - will remove in the future
                company = self.uob.user_details.company.all()[0]
                self.uob.user_details.update( logged_in_as_company = company )
                tech_group_name = slugify(company.company_name)+"__tech__"+str(company.company_id)
                _group_, _created_ = Group.objects.get_or_create(name=tech_group_name)
                _group_.user_set.add(self.uob)
                self.logged_in_as_company = company

            logged_in_company_id = str(self.logged_in_as_company.company_id)

            for ii in self.part_of_groups:
                if ("company_" in ii.name):
                    company_and_role = ii.name.split("__")
                    company_id_hex = company_and_role[-1]
                    role = company_and_role[1]
                    if (company_id_hex==logged_in_company_id):
                        roles_and_scope['logged_in_as'].append({'company':self.logged_in_as_company, "name":ii.name, "company_id":company_id_hex, "role":role })
                        
                else:
                    role = ii.name
                    roles_and_scope['other_roles'].append( { "role": role } )

        except ObjectDoesNotExist:
            self.logged_in_as_company = None
            print({ "error":"User details do not exisit, you need to create a user","code":1 })

        self.roles_and_scope = roles_and_scope
            
        return roles_and_scope

    def get_roles_and_scope(self):
        return self.roles_and_scope

    def get_company_scope(self):
        """Get the company object that the user is logged in as so this can be used to control the scope of what is returned"""
        return self.logged_in_as_company

    def is_admin(self):
        return any([True for ii in self.roles_and_scope['logged_in_as'] if ii['role']=='admin'])

    def is_technician(self):
        return any([True for ii in self.roles_and_scope['logged_in_as'] if ii['role']=='tech']) 

    def is_superadmin(self):
        return any([True for ii in self.roles_and_scope['logged_in_as'] if ii['role']=='superadmin'])

    def is_system_admin(self):
        return any([True for ii in self.roles_and_scope['other_roles'] if ii['role']=='sysadmin'])

    def is_global_admin(self):
        return any([True for ii in self.roles_and_scope['other_roles'] if ii['role']=='globaladmin'])

    def check_auth_admin(self):
        self.get_companies_and_permissions()
        list_of_company_ids = []
        for pm in self.companies_and_permissions: # go through each company they are part of and build up the bundle
            if "admin" in pm["permissions"]:
                list_of_company_ids.append( uuid.UUID(pm["company_id"]) )
        if len(list_of_company_ids) == 0:
            return (False, list_of_company_ids)
        else:
            return (True, list_of_company_ids)

    def check_auth_tech(self):
        self.get_companies_and_permissions()
        list_of_company_ids = []
        for pm in self.companies_and_permissions: # go through each company they are part of and build up the bundle
            if "tech" in pm["permissions"]:
                list_of_company_ids.append( uuid.UUID(pm["company_id"]) )
        if len(list_of_company_ids) == 0:
            return (False, list_of_company_ids)
        else:
            return (True, list_of_company_ids)
            

            
def keep_fields(bundle,fields):
    """Filter out fields from a user for security reasons"""
    data_bundle = {}
    for bb in fields:
        try:
            data_bundle[bb] = bundle.data[bb]
        except:
            pass
    bundle.data = data_bundle
    return bundle


def only_keep_fields(data,fields):
    """Filter out fields from a user for security reasons"""
    datakeep = {}
    for bb in fields:
        try:
            datakeep[bb] = data[bb]
        except:
            pass
            
    return datakeep

def required_fields(data, fields):
    fields_submitted = data.keys()
    fields_required = fields
    ok=all(ff in fields_submitted for ff in fields_required)
    if ok is True:
        return True
    else:
        raise_custom_error({"error":"You have not submitted the required fields"}, 500 )

def if_empty_fill_none(data,fields):
    dataout = {}
    for ff in fields:
        try:
            dataout[ff] = data[ff]
        except:
            dataout[ff] = None
    return dataout

def map_fields(data,fields_to_map):
    """If you need to change the fields in a dictionary to different keys
    The fields_to_map needs to be a list of tuples with the fields (before, after) """
    for jj in fields_to_map: 
        try:
            data[jj[1]] = data[jj[0]]
            del data[jj[0]]
        except:
            pass
    return data


def remove_fields(bundle,fields):
    for ff in fields:
        bundle.data.pop(ff, None)
    return bundle

def remove_fields_from_dict(data,fields):
    for ff in fields:
        data.pop(ff, None)
    return data

def datetime_to_string(date_obj):
    try:
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""

def error_handle_wrapper(func):
    try:
        return func(*args,**argv)
    except:
        return ""

def to_serializable(val):
    try:
        if isinstance(val, datetime.datetime):
            return (val.isoformat() + "Z", None)
        elif isinstance(val, Enum):
            return (val.name, None)
        elif isinstance(val, Point):
            return (val[0],val[1])
        elif attr.has(val.__class__):
            return (attr.asdict(val),0)
        elif isinstance(val, Exception):
            return {
                "error": val.__class__.__name__,
                "args": val.args,
            }
        return (str(val),None)
    except:
        return (None,None)


def parse_string_extract_filter(sort_string, key_words):

    order_by = []
    to_filter = {}
    limit_value = None
    page_value = None
    tokens = sort_string.split('&')
    #pdb.set_trace()
    for token in tokens:
        for field in key_words['fields']:
            if field in token:
                split_token = token.split("=")
                value_raw = split_token[1]
                keyword = split_token[0]
                try:
                    value = float(value_raw)
                    if value.is_integer():
                        value = int(value)
                except:
                    if (value_raw == 'false'):
                        value = False
                    elif (value_raw == 'true'):
                        value = True
                    else:
                        value = str(value_raw)

                if keyword not in key_words['actions']:
                    to_filter[keyword] = value
                
        
        if 'order_by' in token:
            #pdb.set_trace()
            split_token = token.split("=")
            order_by.append(split_token[1])

        if 'limit' in token:
            paginate = True
            split_token = token.split("=")
            limit_value = int(split_token[1])

        if 'page' in token:
            split_token = token.split("=")
            page_value = int(split_token[1])

    return { "order_by":order_by, "limit":limit_value, "page":page_value, "filter":to_filter }

def get_enum_id(enum, object_id):
    try:
        dict_list = enum.__members__
        return dict_list[object_id].value
    except:
        return None

def validate_data(validation_schema, data, error_handler = None ):
    if error_handler is None:
        vv= Validator(validation_schema)
    else:
        vv= Validator(validation_schema, error_handler=error_handler )

    if not vv.validate(data):
        errors_to_report = vv.errors
        raise CustomBadRequest( code="field_error", message=errors_to_report )
    

class AddressSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    id = serpy.IntField()
    country = serpy.Field()
    continent = serpy.Field()
    region = serpy.Field()
    district = serpy.Field()
    ward = serpy.Field()
    village = serpy.Field()
    population = serpy.Field()

class NestedCompany(serpy.Serializer):
    company_id= serpy.Field()
    company_name = serpy.Field()
    country = serpy.Field()
    region = serpy.Field()

class CardTemplateSerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.Field()
    title = serpy.Field()
    description = serpy.Field()
    card_type = serpy.Field()
    entity_type = serpy.Field()
    image = serpy.Field()

class NestedUser(serpy.Serializer):
    id = serpy.IntField()

class NestedUserDetail(serpy.Serializer):
    first_name = serpy.Field()
    last_name = serpy.Field()
    user = NestedUser()

class NestedTemplate(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.Field()

class NestedPendingAction(serpy.Serializer):
    id = serpy.IntField()
    is_complete = serpy.Field()
    entity_type = serpy.Field()
    message = serpy.Field()
    alert_type = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()

class CardSerializerNoPending(serpy.Serializer):
    id = serpy.IntField()
    user = NestedUserDetail()
    card_template = NestedTemplate()
    value = serpy.Field()
    position = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()

class TemplateCardSerializer(serpy.Serializer):
    id = serpy.IntField()
    company = NestedCompany()
    name = serpy.Field()
    title = serpy.Field()
    template_id = serpy.Field()
    description = serpy.Field()
    card_type = serpy.Field()
    entity_type = serpy.Field()
    image = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()

class CardSerializerPending(serpy.Serializer):
    id = serpy.IntField()
    card_template = NestedTemplate()
    user = NestedUserDetail()
    value = serpy.Field()
    pending_actions = serpy.MethodField()
    position = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()

    def get_pending_actions(self, obj):
        return [{"is_complete":jj.is_complete, "message":jj.message , "alert_type":jj.alert_type.name ,"created":jj.created.strftime("%Y-%m-%dT%H:%M:%S") ,"updated":jj.updated.strftime("%Y-%m-%dT%H:%M:%S")} for jj in obj.pending_actions.all()]
        #pending_actions = NestedPendingAction()

class NestedContactSerializer(serpy.Serializer):
    id = serpy.IntField()
    first_name = serpy.Field()
    surname = serpy.Field()
    mobile  = serpy.Field()
    email = serpy.Field()

class BiogasPlantSerialiser(serpy.Serializer):
    id = serpy.Field()
    plant_id = serpy.Field()
    biogas_plant_name = serpy.Field()
    #constructing_technicians = serpy.Field()
    contact = serpy.MethodField()
    UIC = serpy.Field()
    funding_source_notes = serpy.Field()
    other_address_details = serpy.Field()
    type_biogas = serpy.Field()
    supplier = serpy.Field()
    volume_biogas = serpy.Field()
    location_estimated = serpy.Field()
    location = serpy.MethodField()
    QP_status = serpy.Field()
    current_status = serpy.Field()
    notes = serpy.Field()

    def get_location(self, obj):
        return to_serializable(obj.location)

    def get_contact(self, obj):
        return [ {"first_name": ii.first_name, "surname": ii.surname, "mobile": ii.mobile } for ii in obj.contact.all() ]
    
class BiogasPlantIDSerialiser(serpy.Serializer):
    id = serpy.Field()


class JobHistorySerialiser(serpy.Serializer):
    plant = BiogasPlantIDSerialiser()
    fixers = serpy.MethodField()
    accepted_but_did_not_visit = serpy.MethodField()
    rejected_job = serpy.MethodField()
    job_id = serpy.Field()
    date_flagged = serpy.Field()
    date_accepted = serpy.Field()
    date_completed = serpy.Field()
    completed = serpy.Field()
    dispute_raised = serpy.Field()
    job_status = serpy.Field() # Enum field
    verification_of_engagement = serpy.Field()
    fault_description = serpy.Field()
    other = serpy.Field()
    client_feedback_star = serpy.Field()
    client_feedback_additional = serpy.Field()
    overdue_for_acceptance = serpy.Field()
    priority = serpy.Field()
    fault_class = serpy.Field()
    assistance = serpy.Field()
    description_help_need = serpy.Field()
    reason_abandoning_job = serpy.Field()

    def get_fixers(self, obj):
        return [ {"id":ii.id} for ii in obj.fixers.all() ]

    def get_rejected_job(self, obj):
        return [ {"id": ii.id} for ii in obj.rejected_job.all() ]
    
    def get_accepted_but_did_not_visit(self, obj):
        return [ {"id": ii.id} for ii in obj.accepted_but_did_not_visit.all() ]

class IndicatorsTemplateSerialiser(serpy.Serializer):
    id = serpy.Field()
    template_id = serpy.Field()
    type_indicator = serpy.Field()
    title = serpy.Field()
    description = serpy.Field()
    units = serpy.Field()
    image = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()


class IndicatorObjectsSerialiser(serpy.Serializer):
    id = serpy.Field()
    indicator_template = IndicatorsTemplateSerialiser()
    biogas_plant = serpy.Field()
    value = serpy.Field()
    info = serpy.Field()
    status = serpy.Field()
    created = serpy.Field()
    updated = serpy.Field()