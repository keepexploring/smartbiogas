# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 08:49
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0022_auto_20180208_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='techniciandetail',
            name='languages_spoken',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
    ]
