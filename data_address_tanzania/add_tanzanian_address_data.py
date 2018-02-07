import json
import os
import django
from django.contrib.gis.geos import GEOSGeometry
os.environ["DJANGO_SETTINGS_MODULE"] = 'django_react.settings'
django.setup()

from django_dashboard.models import AddressData
import pdb

data_file = 'wards_villages_location2.csv'
#data_ = ' '.join([line.strip() for line in open(data_file, 'r')])
  
#data = json.loads(data_)
#data = json.load( open('address_data.json') )
with open(data_file) as f:
    data =[line.split() for line in f]
#pdb.set_trace()
headings = data[0][0].split(",")
dat_dict = [{headings[k]:value for k, value in enumerate(i[0].split(","))} for i in data[1:]] # 
#pdb.set_trace()
dat = []
#p=0
#for i in data[1:]:
#    dat.append({headings[k]:value for k, value in enumerate(i[0].split(","))})
 #   p=p+1
 #   print(p)
#{headings[0]:i[0].split(",")[0] , headings[1]:i[0].split(",")[1], headings[2]:i[0].split(",")[2], headings[3]:i[0].split(",")[3] , headings[4]:i[0].split(",")[4],  headings[5]:i[0].split(",")[5], headings[6]:i[0].split(",")[6], headings[7]:i[7]}

def add_address_details_to_database(data):
    #pdb.set_trace()
    
    to_insert = []
    for ee,dd in enumerate(data):
        AA = AddressData()
        try:
            _coordinate_ = "POINT(%s %s)" % (dd["wLongitude"],dd["wlatitude"])
        except:
            pdb.set_trace()
            pass
        
        AA.id=dd["id"]
        AA.country="Tanzania"
        AA.continent="Africa"
        AA.region=dd["region"]
        AA.district=dd["district"]
        AA.ward=dd["ward_shehia"]
        AA.village=dd["village_mtaa"]
        AA.lat_long = GEOSGeometry(_coordinate_, srid=4326)
        to_insert.append(AA)
    AddressData.objects.bulk_create(to_insert)
        



if __name__ == '__main__':
    add_address_details_to_database(dat_dict)