# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-16 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0027_auto_20180215_2039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobhistory',
            old_name='completedjob',
            new_name='completed',
        ),
    ]
