# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0023_techniciandetail_languages_spoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='biogasplant',
            name='install_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
