# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-06 07:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0094_auto_20180802_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicatorobjects',
            name='info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
