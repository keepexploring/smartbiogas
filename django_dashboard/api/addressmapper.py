from django_dashboard.models import AddressLocation
import pdb

addressmappings = {
             'tanzania': {
                        'id':'id',
                        'building_name_number':'building_name_number',
                         'address_line1':'neighbourhood',
                         'address_line2':'district',
                         'address_line3':'ward',
                         'region':'region',
                         'city':'village',
                         'zip_code':'postcode',
                         'country':'country',
                         'other':'other_address_details',
                         'continent':'continent',
                         'latitude':'latitude',
                         'longitude':'longitude',
                         'srid':'srid'
                         }

            }
        

def mapaddress(addressobject,country,field,value):
    mapping = AddressMapping.object.filter(country=country)

def get_address_keywords():
    list_mapper_objects = []
    for country in addressmappings.keys():
        list_mapper_objects.append( addressmappings[country].keys() )
        list_mapper_objects.append( addressmappings[country].values() )
    return sum(list_mapper_objects,[])

class AddressObject(object):
    latitude = None
    longitude = None
    srid =  4326

    def set_location(self,longitude, latitude, srid=4326):
        self.latitude = latitude
        self.longitude = longitude
        self.srid =  srid

def create_address_object():
    return type('AddressLocation', (AddressObject, ), {})

def map_address_to_database(address_object):
    address = AddressLocation()
    keys_by_conutry = {country:addressmappings[country].values() for country in addressmappings.keys()}
    address_attributes = [ii for ii in dir(address_object) if not hasattr(getattr(address_object, ii),'__call__') and not ii.startswith('__')]
    try:
        country = address_object.country.lower() # convert output to lowercase
    except:
        raise Exception("Country needs to be an attribute of the address object in order to do the mapping")

    try:
        reverse_address_mappings = { v: k for k, v in addressmappings[country].iteritems() }
    except:
        raise Exception("Country is not available on the system")

    for ii in address_attributes:
        setattr( address,reverse_address_mappings[ii],getattr(address_object,ii) )
    return address

def map_database_to_address_object(address_object):
    address_attributes = [ii.name for ii in address_object._meta.fields]
    address_object_new = create_address_object()
    address_object_instance = address_object_new()
    try:
        country = address_object.country.lower() # convert output to lowercase
    except:
        raise Exception("Country needs to be an attribute of the address object in order to do the mapping")
    address_mapping = addressmappings[country]

    for addattr in address_attributes:
        setattr( address_object_instance, address_mapping[addattr], getattr(address_object,addattr) )
    #getattr(address_object,addattr) for addattr in address_attributes
    #address_object_new = { address_mapping[addattr]:getattr(address_object,addattr) for addattr in address_attributes }
    return address_object_instance

def map_address_to_json_from_database(address_object):
    try:
        country = address_object.country.lower() # convert output to lowercase
    except:
        raise Exception("Country needs to be an attribute of the address object in order to do the mapping")

    #address_attributes = [i for i in dir(address_object) if not inspect.ismethod(i) and not i.startswith('__')]
    address_attributes_to_map = [ ii for ii in addressmappings[country].keys() if ii not in ['id','latitude','longitude','srid'] ]
    address_object_json = { addressmappings[country][addattrib]:getattr(address_object,addattrib) for addattrib in address_attributes_to_map }
    return address_object_json

def map_serialised_address(json_to_map):
    try:
        address_to_map = json_to_map['address']
        country = address_to_map['country'].lower() # convert output to lowercase
        json_to_map['address'] = { addressmappings[country][key]:item for key, item in address_to_map.iteritems() }
        return json_to_map
    except:
        return json_to_map


    

     
# import inspect
# aa=type('Foo', (object, ), {'apple':4,'orange':3}) # creating an object dynamically
# [i for i in dir(aa) if not inspect.ismethod(i) and not i.startswith('__')]

# see https://dynamic-models.readthedocs.io/en/latest/
# create an object dynamically for the address data coming in
# use a setter function to map this to the