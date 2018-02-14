import json

from tastypie.exceptions import TastypieError
from tastypie.http import HttpBadRequest


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

def get_companies_and_permissions(group_list):
    companies_and_permissions = []
    for ii in group_list:
        data = extract_company_id(ii.name)
        exists = check_if_exists(companies_and_permissions,data["company_id"])
        if (exists[0]==True):
            companies_and_permissions[exists[2]]["permissions"] =  companies_and_permissions[exists[2]]["permissions"] + data["permissions"]
        else:
            companies_and_permissions.append(data)

    return companies_and_permissions

            
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