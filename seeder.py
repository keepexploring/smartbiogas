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

#seeder = Seed.seeder()
reg = AddressData.objects.all().values_list('region').distinct()
regions = [i[0] for i in reg]

dist = AddressData.objects.all().values_list('district').distinct()
districts = [i[0] for i in dist]

wrd = AddressData.objects.all().values_list('ward').distinct()
wards = [i[0] for i in wrd]

vill = AddressData.objects.all().values_list('village').distinct()
villages = [i[0] for i in wrd]

continent = 'Africa'
country = 'Tanzania'


pdb.set_trace()
pass

 fixture1 = AutoFixture(Company, field_values={'company_name': names.get_full_name()+"'s biogas company",
                 'country': country,
                 'region': random.choice(regions),
                'district': random.choice(districts),
                'ward': random.choice(wards),
                'village': random.choice(villages),
                'other_address_details':"",
                'emails': fake.email(),
                'neighbourhood':"",
                'other_address_details':"",
                'postcode':"",
                "phone_number":fake.phone_number(),
                "other_info":""
    } )

entries=fixture1.create(30)

fixture2 = AutoFixture(UserDetail, 
    field_values={
        'first_name':fake.first_name(),
        'last_name': fake.last_name(),
        'user_photo':
        'phone_number'
        'country'
        'region'
        'district'
        'ward'
        'village'
        'postcode'
        'neighbourhood'
        'other_address_details'
        
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