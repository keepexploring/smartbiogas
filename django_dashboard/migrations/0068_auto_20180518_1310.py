# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-18 13:10
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0067_biogasplant_thingboard_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardorder',
            name='card_order',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, size=2), blank=True, size=None),
        ),
    ]
