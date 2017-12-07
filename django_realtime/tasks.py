from channels import Channel, Group
from django_dashboard.models import AggregatedStatistics
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, periodic_task
from random import randint
from time import sleep


@db_periodic_task(crontab(minute='1'))
def send_data_update():
    data = AggregatedStatistics().get_data() # get data from a backend model that we need to update
    for i in range(0,5):
        Group('hellothere').send({"text":data},immediately=True)
        sleep(5)

