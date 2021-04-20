# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 16:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0075_auto_20180524_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autofault',
            old_name='auto_fault_detection_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='autofault',
            old_name='auto_fault_detection',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='biogassensorstatus',
            old_name='sensor_status_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='biogassensorstatus',
            old_name='sensor_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='dataconnection',
            old_name='data_connection_with_plant_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='dataconnection',
            old_name='data_connection_with_plant',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='lowgaspressure',
            old_name='low_gas_pressure_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='lowgaspressure',
            old_name='low_gas_pressure_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='trendchangedetectionpdecrease',
            old_name='trend_change_detection_pdecrease_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='trendchangedetectionpdecrease',
            old_name='trend_change_detection_pdecrease',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='trendchangedetectionpincrease',
            old_name='trend_change_detection_pincrease_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='trendchangedetectionpincrease',
            old_name='trend_change_detection_pincrease',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='utilisationstatus',
            old_name='utilisation_status_info',
            new_name='info',
        ),
        migrations.RenameField(
            model_name='utilisationstatus',
            old_name='utilisation_status',
            new_name='status',
        ),
    ]