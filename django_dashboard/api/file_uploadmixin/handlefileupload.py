import os
import django
from django.conf import settings

import uuid

media_root = settings.MEDIA_ROOT
def handle_uploaded_file(ff,file_type):
    image_uuid = uuid.uuid4().hex
    with open(media_root + '/' + image_uuid + '.'+ file_type, 'wb+') as destination:
        for chunk in ff.chunks():
            destination.write(chunk)