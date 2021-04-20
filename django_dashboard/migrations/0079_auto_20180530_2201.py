# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-30 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0078_auto_20180530_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biogasplantcontact',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biogasplantcontact', to='django_dashboard.Address'),
        ),
    ]