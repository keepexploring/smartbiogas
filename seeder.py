#from django_seed import Seed
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'django_react.settings'
django.setup()
import names
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlantContact, JobHistory, Dashboard, Messages, AddressData 
from autofixture import AutoFixture
#from mimesis import Address, Person
from faker import Faker
import random
import requests
import pdb

fake = Faker()
pdb.set_trace()
#seeder = Seed.seeder()
data = AddressData.objects.all().values()
N=20
#address_data = [i for i in data]

#dist = AddressData.objects.all().values_list('district').distinct()
#districts = [i[0] for i in dist]

#wrd = AddressData.objects.all().values_list('ward').distinct()
#wards = [i[0] for i in wrd]

#3vill = AddressData.objects.all().values_list('village').distinct()
#villages = [i[0] for i in wrd]

#continent = 'Africa'
#country = 'Tanzania'

for i in range(0,N):
    data_sample = random.choice(data)
    fixture1 = AutoFixture(Company, field_values={'company_name': names.get_full_name()+"'s biogas company",
                    'country': country,
                    'region': data_sample['region'],
                    'district':data_sample['district'],
                    'ward':data_sample['ward'] ,
                    'village':data_sample['village'] ,
                    'emails':fake.email() ,
                    'neighbourhood':"",
                    'other_address_details':"",
                    'postcode':"",
                    "phone_number":fake.phone_number(),
                    "other_info":""
        } )

    entries=fixture1.create(1)

data_sample = random.choice(data)
fixture2 = AutoFixture(UserDetail, 
    field_values={
        'first_name':fake.first_name(),
        'last_name': fake.last_name(),
        'user_photo': "",
        'phone_number':fake.phone_number(),
        'country': country,
        'region': data_sample['region'],
        'district':data_sample['district'],
        'ward':data_sample['ward'],
        'village':data_sample['village'],
        'postcode':"",
        'neighbourhood':"",
        'other_address_details':""
        
    })

ficture3 = AutoFixture(TechnicianDetail, 
    field_values={


    })

fixture4 = AutoFixture(BiogasPlantContact,
    field_values={

    })

fixture5 = AutoFixture(JobHistory,
    field_values={

    })

fixture6 = AutoFixture(Dashboard,
    field_values={

    })

fixtures7 =AutoFixture(Messages,
    field_values={

    })

#seeder.add_entity(Company, 10, {
#    'company_name': names.get_full_name()+"'s biogas company"
#})

#inserted_pks = seeder.execute()