# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-06 16:59
from __future__ import unicode_literals

from django.db import migrations
import django_dashboard.enums.BiogasPlant
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0014_biogasplant_volume_biogas'),
    ]

    operations = [
        migrations.AddField(
            model_name='biogasplant',
            name='QP_status',
            field=enumfields.fields.EnumField(enum=django_dashboard.enums.BiogasPlant.QPStatus, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='biogasplant',
            name='current_status',
            field=enumfields.fields.EnumField(enum=django_dashboard.enums.BiogasPlant.CurrentStatus, max_length=1, null=True),
        ),
    ]
