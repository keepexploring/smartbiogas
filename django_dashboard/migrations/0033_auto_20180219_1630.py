# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 16:30
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0032_auto_20180219_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingjobs',
            name='technicians_rejected',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='pendingjobs',
            name='accepted',
            field=models.BooleanField(db_index=True, default=None),
        ),
    ]