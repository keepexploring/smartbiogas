import requests
#import numpy as np
from tinynumpy import tinynumpy as np
import json
import pdb
import os
#import ConfigParser

#BASE_DIR = os.path.normpath(os.path.normpath(os.getcwd() + os.sep + os.pardir)+ os.sep + os.pardir)
#BASE_DIR = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ os.sep + os.pardir)
#_BASE_DIR_ = settings.BASE_DIR
#Config = ConfigParser.ConfigParser() # we store security setting in another file
#Config.read(BASE_DIR+'/config/configs.ini')


root_url = "http://localhost:6000"
url_login = root_url + "/token_generation"
url_get_data= root_url + "/get_data"
url_get_devices = root_url + "/get_devices"
url_get_customers = root_url + "/get_customers"
url_check_authenticated = root_url +"/token_authenticated"
auth_headers = {"Authorization":"Bearer","Content-Type":"application/json"}
login_headers = {"Content-Type":"application/json"}
#login_body = {"username":"smartbiogas", "password":"fGCEp9ZqEW5tsmYsRAGQiLD267Ae"}
#login_body = { "username":username, "password":password }

class get_push_data():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.login_body = {}
        self.login_body["username"] = self.username
        self.login_body["password"] = self.password

    def login(self):
        rr = requests.post(url_login, data=json.dumps(self.login_body), headers=login_headers)

        if rr.status_code == 200:
            self.token = rr.json()['token']
            auth_headers["Authorization"] = "Bearer " + str(self.token)
            return True
        else:
            return False

    def check_logged_in(self):
        rr = requests.get(url_check_authenticated, headers = auth_headers)
        if rr.status_code == 200:
            return True
        else:
            return False

    def log_in_if_not(self):
        if self.check_logged_in() is True:
            flag = 1
        else:
            logged_in = self.login()
            if logged_in is True:
                flag = 1
            else:
                flag = 0
        return flag
    
    def get_all_customers(self):
        flag = self.log_in_if_not()
        rr = requests.get(url_get_customers,headers=auth_headers)
        customers = rr.json()
        customer_list = []
        for cc in customers["data"]:
            customer_list.append(cc["customer_id"])

        return customer_list

    def get_all_devices(self,customer_id):
        flag = self.log_in_if_not()
        devices_header = { "customer_id":str(customer_id) }
        rr = requests.post(url_get_devices,data=json.dumps(devices_header), headers=auth_headers)
        if rr.status_code == 200:
            devices = rr.json()
            device_list = []
            for dd in devices['data']:
                device_list.append( { "device_id":dd["device_id"], "name":dd["name"], "customer_id":dd["customer_id"] } )

        return device_list


    def get_data(self, startT, endT, keys= ['PR'] ): # this should be done as a generater expression and be the main one we access
        flag = 0
        
        flag = self.log_in_if_not()

        if (flag ==1):
            customers = self.get_all_customers()
            devices = []
            for c_id in customers:
                devices = devices + self.get_all_devices( customer_id = c_id )
            data_header = {}
            for _data_ in devices:
                data_header["device_id"] = _data_["device_id"]
                data_header["startT"] = int(startT)
                data_header["endT"] = int(endT)
                rr = requests.post(url_get_data,data=json.dumps(data_header),headers=auth_headers)
                dat = rr.json()
                #pdb.set_trace()
                for key in keys:
                    data_array = self.convert_to_numpy_array( dat[key] )
                    yield( {"key":key,"data_header":data_header["device_id"],"name":_data_["name"], "data":data_array} )
        else:
            yield("error")

    
    

    def get_data_for_device(self, device_id, name, startT, endT, keys= ['PR'] ):

        flag = self.log_in_if_not()

        data_header = {}
        data_header["device_id"] = str(device_id)
        data_header["startT"] = int(startT)
        data_header["endT"] = int(endT)
        rr = requests.post(url_get_data,data=json.dumps(data_header),headers=auth_headers)
        dat = rr.json()

        for key in keys:
            yield dat[key]
            #data_array = self.convert_to_numpy_array( dat[key] )
            #yield( {"key":key,"data_header":data_header["device_id"],"name":name, "data":data_array} )
            
    def convert_to_numpy_array( self, dat ):
        #pdb.set_trace()
        np_data = []
        for ii in dat:
            np_data.append( [ ii["ts"], ii['value'] ] )

        return np.array(np_data)



if __name__ == '__main__':
    api = get_push_data(username='smartbiogas', password='fGCEp9ZqEW5tsmYsRAGQiLD267Ae')
    customers = api.get_all_customers()
    devices = api.get_all_devices(customer_id=customers[0])
    bb= 'apples'
    data = api.get_data_for_device(device_id=devices[0]['device_id'], name='SBN7', startT=1513987200000, endT=1514160000000 )
    print(next(data))
    #aa=next(data_to_get.get_data(startT = 1513987200000, endT = 1514160000000))
    


# [{'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN7', 'device_id': u'1e7e59ddc13c9c09e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN3', 'device_id': u'1e7e59ddace78809e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN9', 'device_id': u'1e7e59ddb84f7409e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN5', 'device_id': u'1e7e59ddce830c09e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'ECHO_HUB', 'device_id': u'1e7e59cf8d46f209e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN4', 'device_id': u'1e7e59ddd4b5f609e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN6', 'device_id': u'1e7e59dda491be09e6a33a31860bc0d'}, {'customer_id': u'1e7f13f89cd0d40873c33a31860bc0d', 'name': u'SBN0', 'device_id': u'1e7e59ddc82b8309e6a33a31860bc0d'}]