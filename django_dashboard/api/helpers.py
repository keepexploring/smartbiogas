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

class Permissions():

    def __init__(self, part_of_group):
        self.part_of_group = part_of_group

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
    name = serpy.Field()
    title = serpy.Field()
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
    