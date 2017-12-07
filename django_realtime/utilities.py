
from channels import Channel, Group
from django_dashboard.models import AggregatedStatistics
import json
from time import sleep



def send_data():
    while True:
        data=AggregatedStatistics().get_data()
        Group("hellothere").send({"text": json.dumps(data)},immediately=True)
        sleep(5)
