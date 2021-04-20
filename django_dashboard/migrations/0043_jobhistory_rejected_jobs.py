# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-01 18:53
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0042_auto_20180301_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobhistory',
            name='rejected_jobs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
    ]