
from country_data import country_data
import json
import pdb

data_dict = {}


for dd in country_data:
    data_dict[ dd["cca2"] ] = dd
pdb.set_trace()
with open('/Users/Joel/Documents/CREATIVenergie/Dashboard2/SmartBiogas6/django_dashboard/api/country_data.json', 'w') as fp:
    json.dump(data_dict, fp)

