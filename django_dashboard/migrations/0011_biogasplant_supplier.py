# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-06 14:54
from __future__ import unicode_literals

from django.db import migrations
import django_dashboard.enums.BiogasPlant
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0010_auto_20180202_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='biogasplant',
            name='supplier',
            field=enumfields.fields.EnumField(enum=django_dashboard.enums.BiogasPlant.SupplierBiogas, max_length=1, null=True),
        ),
    ]
