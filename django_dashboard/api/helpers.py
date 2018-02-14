import json

from tastypie.exceptions import TastypieError
from tastypie.http import HttpBadRequest
import uuid


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
            data = extract_company_id(ii.name)
            exists = check_if_exists(self.companies_and_permissions,data["company_id"])
            if (exists[0]==True):
                self.companies_and_permissions[exists[2]]["permissions"] =  self.companies_and_permissions[exists[2]]["permissions"] + data["permissions"]
            else:
                self.companies_and_permissions.append(data)

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