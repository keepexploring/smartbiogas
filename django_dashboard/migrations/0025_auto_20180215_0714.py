# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-15 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0024_biogasplant_install_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobhistory',
            old_name='priority',
            new_name='_assistance',
        ),
        migrations.RenameField(
            model_name='jobhistory',
            old_name='completed',
            new_name='_completed',
        ),
        migrations.AddField(
            model_name='jobhistory',
            name='_priority',
            field=models.NullBooleanField(default=False),
        ),
    ]
