# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-18 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0066_biogasplant_thingboard_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='biogasplant',
            name='thingboard_ref',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
