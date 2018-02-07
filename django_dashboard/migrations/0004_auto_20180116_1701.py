# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 17:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0003_auto_20180116_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressData',
            fields=[
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.IntegerField(blank=True, null=True)),
                ('region', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('district', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('ward', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('village', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('lat_long', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, geography=True, null=True, srid=4326)),
                ('population', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='biogasplantcontact',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='biogasplantcontact',
            name='surname',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
