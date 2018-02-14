#from django_seed import Seed
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'django_react.settings'
django.setup()
import names
from django_dashboard.models import Company, UserDetail, TechnicianDetail, BiogasPlant, BiogasPlantContact, JobHistory, Dashboard, Messages, AddressData 
from django.contrib.auth.models import User
from autofixture import AutoFixture
#from mimesis import Address, Person
from faker import Faker
import random
import requests
import what3words
from os import environ
import requests
import shortuuid
import uuid
from django.core import files
import tempfile
import re

import pdb
w3w = what3words.Geocoder('R35K949K')

fake = Faker()

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

continent = 'Africa'
country = 'Tanzania'

def random_phone_number():
    #x=random.randint(10,99)
    x='255' # for Tanzania
    y=random.randint(1000000000,9999999999)
    num = '+'+x+str(y)
    return num

def create_companies():
    for i in range(0,N):
        #pdb.set_trace()
        data_sample = random.choice(data)
        company_name = fake.name() + "'s biogas company"
        fixture1 = AutoFixture(Company, field_values={'company_name':company_name,
                        'country': country,
                        'region': data_sample['region'],
                        'district':data_sample['district'],
                        'ward':data_sample['ward'] ,
                        'village':data_sample['village'] ,
                        'emails':[fake.email()],
                        'neighbourhood':"",
                        'other_address_details':"",
                        'postcode':"",
                        "phone_number":random_phone_number(),
                        "other_info":""
            } )
        

        entries1=fixture1.create(1)

def create_users():
    for i in range(0,N):
        first_name = fake.first_name()
        last_name = fake.last_name()
        ran = shortuuid.ShortUUID().random(length=3)
        username = first_name+last_name+ran
        fixture_users = AutoFixture(User, field_values={
                'username':username,
                'first_name':first_name,
                'last_name':last_name,
                'password':'abc123',
                'is_staff':False,
                'is_active':True,
                'is_superuser':False,
                'email':fake.email()

        })
        entries_users=fixture_users.create(1)

def create_user_detail():
    for i in range(0,N):
        data_sample = random.choice(data)
        url_list=['https://randomuser.me/api/portraits/women','https://randomuser.me/api/portraits/men']
        image_url=random.choice(url_list)+"/"+str(random.randint(0,100))+'.jpg'
        im = requests.get(image_url, stream=True)
        file_name = image_url.split('/')[-3:]
        file_name = "".join(file_name)
        lf = tempfile.NamedTemporaryFile()
        
        for block in im.iter_content(1024 * 8):
        # If no more file then stop
            if not block:
                break
        
        # Write image block to temporary file
            lf.write(block)
        lf.name = file_name
        #pdb.set_trace()
        fixture2 = AutoFixture(UserDetail, field_values={
                'first_name':fake.first_name(),
                'last_name': fake.last_name(),
                'user_photo': files.File(lf),
                'phone_number':fake.phone_number(),
                'country': country,
                'region': data_sample['region'],
                'district':data_sample['district'],
                'ward':data_sample['ward'],
                'village':data_sample['village'],
                'postcode':"",
                'neighbourhood':"",
                'other_address_details':"",
            } )
        entries2=fixture2.create(1)

def generate_random_location():
    lat_ = random.uniform(-11,-2.193297)
    long_ = random.uniform(29.673386,39.276638)
    return (lat_, long_)

def create_technican_detail():
    for i in range(0,N):
        lat_long = generate_random_location()
        res = w3w.reverse(lat=lat_long[0], lng=lat_long[1])['words']
        willing_to_travel = random.randint(1,30)
        max_num_jobs_allowed = random.randint(1,6)
        av_rating=random.uniform(0,5)
        ficture3 = AutoFixture(TechnicianDetail, 
            field_values={
                'number_jobs_active': random.randint(0,5),
                'number_of_jobs_completed':random.randint(0,100),
                'rating': [{'job_id':1,'user_rating':3}],
                'what3words': res,
                'willing_to_travel':willing_to_travel,
                'max_num_jobs_allowed':max_num_jobs_allowed,
                'average_rating': av_rating
            })
        entries3=ficture3.create(1)

def create_biogas_plants():
    for i in range(0,N):
        lat_long = generate_random_location()
        res = w3w.reverse(lat=lat_long[0], lng=lat_long[1])['words']
        data_sample = random.choice(data)
        volume = ['<3.0m3','3.0m3','4.0m3','5.0m3','6.0m3','7.0m3','8.0m3','9.0m3','10.0m3','11.0m3','12.0m3','>12.0m3']
        fixture4 = AutoFixture(BiogasPlant,
            field_values={
                'country': country,
                'region': data_sample['region'],
                'district':data_sample['district'],
                'ward':data_sample['ward'],
                'village':data_sample['village'],
                'postcode':"",
                'neighbourhood':"",
                'volume_biogas': random.choice(volume),
                'what3words':res
            })
        entries4=fixture4.create(1)

def create_biogas_plant_contact():
    fixture5 = AutoFixture(BiogasPlantContact,
        field_values={
            'first_name':fake.first_name(),
            'surname':fake.last_name(),
            'mobile':random_phone_number(),
            'email':fake.email(),
        })
    entries5=fixture5.create(10)

def create_jobs():
    fixture6 = AutoFixture(JobHistory,
        field_values={
            })
    entries6=fixture6.create(1000)

def create_dashboard_data():
    fixture7 = AutoFixture(Dashboard,
        field_values={
            'plants':random.randint(0,100),
            'active':random.randint(0,100),
            'faults':random.randint(0,100),
            'avtime':random.randint(0,100),
            'jobs':random.randint(0,100),
            'fixed':random.randint(0,100),
        })
    entries6=fixture7.create(10)


# fixtures8 =AutoFixture(Messages,
#     field_values={
#         message_from_num:
#         message_to_num:
#         message_from_email:
#         message_to_email:
#     })

#seeder.add_entity(Company, 10, {
#    'company_name': names.get_full_name()+"'s biogas company"
#})

#inserted_pks = seeder.execute()
def main():
    #create_companies()
    #create_users()
    #create_user_detail()
    #create_technican_detail()
    #create_biogas_plant_contact()
    #create_biogas_plants()
    create_jobs()
    #create_dashboard_data()

    

if __name__ == '__main__':
    main()