# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-14 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0051_auto_20180313_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='company',
            field=models.ManyToManyField(blank=True, to='django_dashboard.Company'),
        ),
    ]
