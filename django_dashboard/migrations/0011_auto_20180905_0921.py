# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-05 09:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0010_auto_20180904_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='editrecord',
            name='who',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='who_edited', to='django_dashboard.UserDetail'),
        ),
    ]
