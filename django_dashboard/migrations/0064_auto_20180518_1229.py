# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-18 12:29
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0063_auto_20180517_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardorder',
            name='card_order',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=None), blank=True, size=None),
        ),
    ]
